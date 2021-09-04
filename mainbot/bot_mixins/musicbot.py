from discord.errors import DiscordException
from discord.player import AudioPlayer, AudioSource
from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit
from ..core.gpt2api import sanitize
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5, ytdl_format_options=ytdl_format_options):
        super().__init__(source, volume)
        youtube_dl.utils.bug_reports_message = lambda: ''
        self.ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')


class MusicMixin(DiscordInit, commands.Cog):
    lastPod = None
    source = None
    Aplayer = None
    IS_PLAYING = False
    PREV_SONG = None
    SONG_QUEUE = []

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(pass_context=True, aliases=['pl', 'plf', 'lf'])
    async def lofi(self, ctx, *, flavour='study'):
        voice_client: discord.VoiceClient = discord.utils.get(
            self.client.voice_clients, guild=ctx.guild)
        await ctx.message.add_reaction(Emotes.LOFISPARKO)
        url = ""
        flavoururls = {
            'study': 'https://www.youtube.com/watch?v=5qap5aO4i9A',
            'sleep': 'https://www.youtube.com/watch?v=DWcJFNfaw9c',
            'violet': 'https://www.youtube.com/watch?v=8mY3Udau4sE',
            'silentvoice': 'https://www.youtube.com/watch?v=Fu9hLWfOups',
            'yourname': 'https://www.youtube.com/watch?v=H9yfuYDoGf4',
            'minecraft': 'https://www.youtube.com/watch?v=Dg0IjOzopYU',
            'disco': 'https://www.youtube.com/watch?v=qz_Yzt_9ZbY',
            'sad': 'https://www.youtube.com/watch?v=yf18K9g-XV0',
            'avec': 'https://www.youtube.com/watch?v=tcjxT3m5UDE'
        }
        async with ctx.typing():
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                info = ydl.extract_info(flavoururls[flavour], download=False)
                url = info['formats'][0]['url']
        embed = discord.Embed(
            title=f"Playing {flavour}", colour=discord.Colour(0xff5065), url=url)
        embed.set_image(
            url=f"https://i.ytimg.com/vi/{flavoururls[flavour][-11:]}/maxresdefault.jpg")
        embed.set_author(name=ctx.message.author.name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=self.name, icon_url=self.avatar)
        await ctx.send(embed=embed, components=[[Button(style=ButtonStyle.red, label="Stop")], ])
        await self.playmp3source(url, context=ctx)

    @commands.command(pass_context=True, aliases=['q'])
    async def queue(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}'s music Queue")
        totquetime = 0
        if(len(self.SONG_QUEUE) > 0):
            for SONGURL in self.SONG_QUEUE:
                totquetime += SONGURL[3]
                embed.add_field(
                    name=f"{SONGURL[1]}", value=f"{SONGURL[3]} mins \nRequested by {SONGURL[2]}", inline=False)
            embed.set_footer(
                text=f"Runtime {totquetime} minutes", icon_url=self.avatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send("> Queue is empty", delete_after=5.0)

    @commands.command(pass_context=True, aliases=['pnq', 'skip', 'next'])
    async def playNextQ(self, ctx):
        if(len(self.SONG_QUEUE) > 0):
            self.SONG_QUEUE.pop(0)
            flavour = self.SONG_QUEUE[0][0]
            await ctx.send(f"> Playing Next Song from queue {self.SONG_QUEUE[0][1]}", delete_after=5.0)
            await ctx.invoke(self.client.get_command('rawplay'), ctx=ctx, temp_flavour=flavour)
        else:
            await ctx.send("> Queue is empty", delete_after=5.0)

    @commands.command(pass_context=True, aliases=['paq'])
    async def addQ(self, ctx, *, flavour):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(flavour, download=False)
        URL = info['formats'][0]['url']
        TITLE = info['title']
        self.SONG_QUEUE.append(
            [URL, TITLE, ctx.author.nick, round(info['duration']/60)])
        await ctx.message.add_reaction("👍")
        await ctx.send(f"> Added {TITLE} to queue", delete_after=5.0)
        return

    @commands.command(pass_context=True, aliases=['play', 'ytp', 'p'])
    async def rawplay(self, ctx, *, flavour='https://www.youtube.com/watch?v=dQw4w9WgXcQ', temp_flavour=None):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if(temp_flavour == None):
            pass
        else:
            flavour = temp_flavour

        if(not voice.is_playing()):
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(flavour, download=False)
            URL = info['formats'][0]['url']
            async with ctx.typing():
                embed = discord.Embed(
                    title=f"**Playing** {info['title']}", colour=find_dominant_color(info['thumbnails'][0]['url']), url=URL, description=f"```{info['description'][:200]} ...```")
                embed.set_image(url=info['thumbnails'][-1]['url'])
                try:
                    embed.add_field(
                        name="Duration", value=f"{int(info['duration']/60)}:{int(info['duration']%60)} mins", inline=True)
                except:
                    embed.add_field(
                        name="Duration", value=f"Streaming Live", inline=True)
                embed.add_field(name="Uploader",
                                value=info['uploader'], inline=True)

                embed.set_author(name=ctx.message.author.name,
                                 icon_url=ctx.message.author.avatar_url)
                embed.set_footer(
                    text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)

            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()

            # make some hacky queue system for songs OwO
            if(len(self.SONG_QUEUE) > 0):
                self.SONG_QUEUE.pop(0)
                flavour = self.SONG_QUEUE[0][0]
                await ctx.invoke(self.client.get_command('rawplay'), flavour=flavour)
            else:
                await ctx.message.add_reaction(Emotes.PACEXCLAIM)
                await ctx.reply("> Queue is empty", delete_after=5.0)

        elif(self.IS_PLAYING):
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(flavour, download=False)
            URL = info['formats'][0]['url']
            TITLE = info['title']
            self.SONG_QUEUE.append(
                [URL, TITLE, ctx.author.nick, round(info['duration']/60)])
            await ctx.send(f"> Added {TITLE} to queue", delete_after=5.0)
            return
        else:
            await ctx.message.add_reaction(Emotes.PACEXCLAIM)
            await ctx.send("> Nothing is playing", delete_after=5.0)

    @commands.command(aliases=['podepi'])
    async def podepisode(self, ctx, epno=0):
        await ctx.message.add_reaction('🔍')
        podepi = epno
        if(self.lastPod == None):
            embed = discord.Embed(
                colour=discord.Colour(0xbd10e0), description=" ")
            embed.set_thumbnail(url=self.avatar)
            embed.set_author(name=self.name, url=self.avatar,
                             icon_url=self.avatar)
            embed.add_field(name=f"No Recent Podcast Searches",
                            value=f"search for podcast using {self.pre}pod", inline=False)
            embed.set_thumbnail(url=self.avatar)
            await ctx.send(embed=embed)
        else:
            currentpod = self.lastPod
            try:
                try:
                    desc = sanitize(currentpod.GetEpisodeDetails(
                        podepi)['summary'][:2250]) + "..."
                except:
                    desc = "No Information Available"
                try:
                    title = currentpod.GetEpisodeDetails(podepi)['title']
                except:
                    title = "404"

                embed = discord.Embed(title=title, colour=find_dominant_color(currentpod.PodcastImage(
                    podepi)), url=currentpod.GetEpisodeDetails(podepi)['link'], description=desc, inline=False)
                try:
                    embed.set_thumbnail(url=currentpod.PodcastImage(podepi))
                except:
                    pass
                try:
                    embed.set_footer(text="Published on " + currentpod.GetEpisodeDetails(
                        podepi)['published'][:16], icon_url=self.avatar)
                except:
                    pass
                await ctx.send(embed=embed)
            except AttributeError:
                await ctx.message.add_reaction(Emotes.PACEXCLAIM)
                await ctx.send("> No Episode found")

    @commands.command(aliases=['podp'])
    async def podplay(self, ctx, epno=0):
        await ctx.message.add_reaction(Emotes.PACPLAY)
        podepi = epno
        if(self.lastPod == None):
            embed = discord.Embed(
                colour=discord.Colour(0xbd10e0), description=" ")
            embed.set_thumbnail(url=self.avatar)
            embed.set_author(name=self.name, url=self.avatar,
                             icon_url=self.avatar)
            embed.add_field(name=f"No Recent Podcast Searches",
                            value=f"search for podcast using {self.pre}pod", inline=False)
            embed.set_thumbnail(url=self.avatar)
            await ctx.send(embed=embed)
        else:
            currentpod = self.lastPod
            try:
                try:
                    desc = sanitize(currentpod.GetEpisodeDetails(
                        podepi)['summary'][:2200]) + "..."
                except:
                    desc = "No Information Available"
                try:
                    title = currentpod.GetEpisodeDetails(podepi)['title']
                except:
                    title = "404"

                embed = discord.Embed(title=title, colour=find_dominant_color(currentpod.PodcastImage(
                    podepi)), url=currentpod.GetEpisodeDetails(podepi)['link'], description=desc, inline=False)
                try:
                    embed.set_thumbnail(url=currentpod.PodcastImage(podepi))
                except:
                    pass
                try:
                    embed.set_footer(text="Published on " + currentpod.GetEpisodeDetails(
                        podepi)['published'][:16], icon_url=self.avatar)
                except:
                    pass
                embed.set_footer(
                    text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, components=[[Button(style=ButtonStyle.red, label="Stop")], ])
                await self.playPodcast(ctx, podepi=podepi, currentpod=currentpod)
            except AttributeError:
                pass

    @commands.command(aliases=['podcast'])
    async def pod(self, ctx, *, strparse=" ", pgNo=0, searchIndex=0):
        if(':' in strparse):
            podname_, num = strparse.replace(' ', '').split(':')
            podepi = int(num)
        elif(not strparse == ' '):
            podname_ = strparse.replace(' ', '')
            podepi = None
        else:
            podname_ = ' '
            podepi = None

        try:
            start = pgNo
            podname = podname_.split('-')[0]
        except:
            start = 0
            podname = podname_
        if(podname == " "):
            embed = discord.Embed(colour=discord.Colour(
                0x91ff), description="Podcast Section")
            embed.set_thumbnail(url=self.avatar)
            embed.set_author(name=self.name, icon_url=self.avatar)
            embed.add_field(
                name=f"{self.pre}pod", value="This very command you ran", inline=False)
            embed.add_field(name=f"{self.pre}pod [Name of Podcast]",
                            value="Searches for the Podcast and shows Episodes related to it.", inline=False)
            embed.add_field(
                name=f"{self.pre}podp [Selection No]", value="Play the podcast selection , plays the latest available episode", inline=False)
            embed.add_field(name=f"{self.pre}podepi [Selection No]",
                            value="Shows the Episode Details for selected episode", inline=False)
            embed.add_field(name=f"{self.pre}stop or {self.pre}dc",
                            value="Stop and Disconnect\n", inline=False)
            embed.add_field(name=f"{self.pre}pause or {self.pre}resume",
                            value="Pause and Resume\n (Havent Implemented Seeking and queueing yet)", inline=False)
        if(podepi == None and not podname == " "):
            await ctx.message.add_reaction('🔍')
            try:
                k = ph.PodSearch(podname, searchIndex=searchIndex)
            except json.JSONDecodeError as e:
                embed = discord.Embed(
                    colour=discord.Colour(0x120012), description=" ")
                embed.set_thumbnail(url=self.avatar)
                embed.set_author(
                    name=self.name, url=self.avatar, icon_url=self.avatar)
                embed.add_field(name=f"Corrupted Feed", value=e, inline=False)
                return
            except:
                embed = discord.Embed(
                    colour=discord.Colour(0x120012), description=" ")
                embed.set_thumbnail(url=self.avatar)
                embed.set_author(
                    name=self.name, url=self.avatar, icon_url=self.avatar)
                embed.add_field(name=f"Somewhere Something went wrong",
                                value=r"I have 0 clue what the hell happened rn ¯\_(ツ)_/¯", inline=False)
                return
            await ctx.message.add_reaction('⏳')
            if(not k['name'] == "Podcast Not Found"):
                currentpod = ph.Podcast(k['name'], k['rss'])
                self.lastPod = currentpod
                paginationsize = ph.Pagination(k['count'], 5)
                try:
                    thiscol = find_dominant_color(k['image'])
                except:
                    thiscol = 0xffffff
                embed = discord.Embed(colour=thiscol, description=" ")
                embed.set_thumbnail(url=self.avatar)
                embed.set_author(
                    name=k['name'], url=k['rss'], icon_url=k['image'])
                ind = 0 + 5*start
                for episode_ in currentpod.ListEpisodes()[start:start+5]:
                    currentEpisodeDetail = currentpod.GetEpisodeDetails(ind)
                    embed.add_field(
                        name=f"{ind} : " + currentEpisodeDetail['title'], value=f"_{currentEpisodeDetail['published'][:15]}_\n ```{sanitize(currentEpisodeDetail['summary'][:80])}...```\n", inline=False)
                    ind += 1
                embed.set_footer(
                    text=f"Page {start+1}/{paginationsize}", icon_url=self.avatar)
                try:
                    embed.set_thumbnail(url=k['image'])
                except:
                    embed.set_thumbnail(url=self.avatar)
            else:
                embed = discord.Embed(
                    colour=discord.Colour(0x120012), description=" ")
                embed.set_thumbnail(url=self.avatar)
                embed.add_field(name=f"No Podcasts Found",
                                value="No Results", inline=False)
                embed.set_thumbnail(url=self.avatar)
            try:
                embed.set_thumbnail(url=currentpod.PodcastImage(podepi))
            except:
                pass

        del_dis = await ctx.send(embed=embed, components=[[Button(style=ButtonStyle.green, label="Play Latest"), Button(style=ButtonStyle.red, label="Prev Page"), Button(style=ButtonStyle.blue, label="Next Page"), Button(style=ButtonStyle.grey, label="Next Search Result")]])

        while True:
            res = await self.client.wait_for("button_click", timeout=100)
            if(await ButtonProcessor(ctx, res, "Play Latest")):
                await ctx.invoke(self.client.get_command('podplay'))
                await del_dis.delete()
                break
            elif(await ButtonProcessor(ctx, res, "Next Page")):
                await del_dis.delete()
                await ctx.invoke(self.client.get_command('pod'), strparse=strparse, pgNo=pgNo+1)
                break
            elif(await ButtonProcessor(ctx, res, "Prev Page") and pgNo > 2):
                await del_dis.delete()
                await ctx.invoke(self.client.get_command('pod'), strparse=strparse, pgNo=pgNo-1)
                break
            elif(await ButtonProcessor(ctx, res, "Next Search Result")):
                await del_dis.delete()
                await ctx.invoke(self.client.get_command('pod'), strparse=strparse, pgNo=0, searchIndex=searchIndex+1)
                break
            elif len(ctx.voice_client.channel.members) < 2:
                await ctx.send("> Dont leave me alone " + ctx.author.mention + Emotes.PACDEPRESS)
                await ctx.voice_client.disconnect()
                break

    async def playPodcast(self, context, podepi, currentpod):
        try:
            await context.voice_client.disconnect()
        except:
            pass

        if context.voice_client is None:
            if context.author.voice.channel:
                await context.author.voice.channel.connect()

        _source_ = currentpod.GetEpisodeMp3(podepi)
        await self.playmp3source(_source_, context=context)

    async def playmp3source(self, mp3link: str, context):
        ctx = context
        voice_client: discord.VoiceClient = discord.utils.get(
            self.client.voice_clients, guild=ctx.guild)
        audio_source = discord.FFmpegPCMAudio(mp3link)
        self.source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(
            mp3link, before_options=ffmpeg_options), volume=100)
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=False, self_deaf=True)

        while ctx.voice_client.is_connected():
            if len(ctx.voice_client.channel.members) == 1:
                await ctx.send("> Dont leave me alone " + Emotes.PACDEPRESS)
                await ctx.voice_client.disconnect()
                break
            elif ctx.voice_client.is_paused():
                await asyncio.sleep(1)
            elif ctx.voice_client.is_playing():
                await asyncio.sleep(1)
                res = await self.client.wait_for("button_click")
                if(await ButtonProcessor(ctx, res, "Stop")):
                    await ctx.invoke(self.client.get_command('stop'))
                    break
                elif(await ButtonProcessor(ctx, res, "Pause")):
                    await ctx.invoke(self.client.get_command('pause'))
                elif(await ButtonProcessor(ctx, res, "Resume")):
                    await ctx.invoke(self.client.get_command('resume'))
            else:
                await ctx.voice_client.disconnect()
                break

    @commands.command(aliases=['pau'])
    async def pause(self, ctx):
        try:
            ctx.voice_client.pause()
            await ctx.message.add_reaction(Emotes.PACPAUSE)
        except:
            await ctx.send(f"> {ctx.author.mention} I see-eth nothing playin")

    @commands.command(aliases=['res'])
    async def resume(self, ctx):
        try:
            await ctx.message.add_reaction(Emotes.PACPLAY)
            ctx.voice_client.resume()
        except:
            await ctx.send(f"> {ctx.author.mention} Nothing's playing")

    @commands.command(aliases=['fuckoff', 'dc', 'disconnect', 'stfu'])
    async def stop(self, ctx):
        if(ctx.author.voice.channel):
            await ctx.message.add_reaction(Emotes.PACSTOP)
            await ctx.voice_client.disconnect()
            self.SONG_QUEUE = []
            return await ctx.reply(f"> stopped playback", delete_after=5.0)
        else:
            await ctx.message.add_reaction(Emotes.PACEXCLAIM)
            return await ctx.reply("> You're not in voice channel", delete_after=5.0)

    @rawplay.before_invoke
    @lofi.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice.channel:
                await ctx.author.voice.channel.connect()
                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=False, self_deaf=True)
            else:
                embed = discord.Embed(
                    title=f"> {ctx.message.author.mention} isn't in any voice channel that I can see mate", colour=discord.Colour(0xff5065))
                embed.set_author(name=ctx.message.author.name,
                                 icon_url=ctx.message.author.avatar_url)
                embed.set_footer(text=self.client.user.name,
                                 icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)

        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(MusicMixin(bot))
