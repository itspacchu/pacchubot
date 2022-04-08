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
import urllib
from musicYeet import FFMPEG_BEFORE_OPTS


class MusicMixin(DiscordInit, commands.Cog):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    lastPod = None
    source = None
    Aplayer = None
    IS_PLAYING = False

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

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
                        name=f"{ind} : " + currentEpisodeDetail['title'], value=f"_{currentEpisodeDetail['published'][:16]}_\n ```{sanitize(currentEpisodeDetail['summary'][:80])}...```\n", inline=False)
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
            mp3link, before_options=FFMPEG_BEFORE_OPTS), volume=80)
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

    @podplay.before_invoke
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