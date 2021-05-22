from ..__imports__ import *
from ..settings import *
from .discord_init import DiscordInit

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5, ytdl_format_options=ytdl_format_options):
        super().__init__(source, volume)
        youtube_dl.utils.bug_reports_message = lambda: ''
        self.ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(self, cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else self.ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class MusicMixin(DiscordInit, commands.Cog):
    StartTime = 0
    lastPod = None

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()


    @commands.command(pass_context=True, aliases=['p', 's'])
    async def play(self, ctx, *, url="https://youtu.be/dQw4w9WgXcQ"):
        await ctx.message.add_reaction('🎧')
        self.StartTime += ttime.time()
        if ("youtube.com" in str(url) or "youtu.be"):
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=None)
                if(str(url) == "https://youtu.be/dQw4w9WgXcQ"):
                    embed = discord.Embed(title="You need to give a url!", colour=discord.Colour(0xff5065), url=url, description=player.title)
                    embed.set_image(url="https://i.imgur.com/xrBXtFh.png")
                else:
                    embed = discord.Embed(title="Playing from Youtube", colour=discord.Colour(0xff5065), url=url, description=player.title)
                    y = re.search("/?v=(.{,11})", url).groups()[0]
                    try:
                        embed.set_image(url=f"https://img.youtube.com/vi/{y}/0.jpg")
                    except:
                        pass
        else:
            embed = discord.Embed(title=f"Searching : {str(url)}", colour=discord.Colour(0xff5065))
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=None)

        embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=self_name, icon_url=self_avatar)
        await ctx.reply(embed=embed)

    @commands.command(pass_context=True, aliases=['pl'])
    async def lofi(self, ctx, *, url="https://youtu.be/5qap5aO4i9A"):
        self.StartTime += ttime.time()
        await ctx.message.add_reaction('🎧')
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=None)
            embed = discord.Embed(title="Playing from Youtube", colour=discord.Colour(0xff5065), url=url, description=player.title)
            embed.set_image(url="https://i.ytimg.com/vi/5qap5aO4i9A/maxresdefault.jpg")
        embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=self_name, icon_url=self_avatar)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['podp'])
    async def podplay(self,ctx,epno=0):
        podepi = epno
        if(self.lastPod == None):
            embed = discord.Embed(colour=discord.Colour(
                0xbd10e0), description=" ")
            embed.set_thumbnail(url=self_avatar)
            embed.set_author(name=self_name, url=self_avatar,icon_url=self_avatar)
            embed.add_field(name=f"No Recent Podcast Searches",value=f"search for podcast using {self.pre}pod",inline=False)
            embed.set_thumbnail(url=self_avatar)
            await ctx.send(embed=embed)
        else:
            currentpod = self.lastPod
            try:
                await self.playPodcast(ctx,podepi=podepi,currentpod=currentpod)
                embed = discord.Embed(title=currentpod.GetEpisodeDetails(podepi)['title'],
                                      colour=discord.Colour(0xb8e986), url=currentpod.GetEpisodeDetails(podepi)['link'],
                                      description=currentpod.GetEpisodeDetails(podepi)['summary'],
                                      inline=False)
                embed.set_thumbnail(url=currentpod.PodcastImage(podepi))
                embed.set_author(name=self_name,icon_url=self_avatar)
                embed.set_footer(text=currentpod.GetEpisodeDetails(podepi)['title'],icon_url=self_avatar)
                await ctx.send(embed=embed)
            except AttributeError:
                await ctx.send("You aren't in voice channel m8")


    @commands.command(aliases=['podcast'])
    async def pod(self,ctx , * , strparse = " "):
        await ctx.message.add_reaction('🔎')
        if(':' in strparse):
            podname_,num = strparse.replace(' ','').split(':')
            podepi = int(num)
        elif(not strparse == ' '):
            podname_ = strparse.replace(' ','')
            podepi = None
        else:
            podname_ = ' '
            podepi = None

        try:
            start = int(podname_.split('-')[1])
            podname = podname_.split('-')[0]
        except:
            start = 0
            podname = podname_


        if(podname == " "):
            embed = discord.Embed(colour=discord.Colour(0x91ff), description="Podcast Section")
            embed.set_thumbnail(url=self_avatar)
            embed.set_author(name=self_name, icon_url=self_avatar)
            embed.add_field(name=f"{self.pre}pod", value="This very command you ran",inline=False)
            embed.add_field(name=f"{self.pre}pod [Name of Podcast]",value="Searches for the Podcast and shows Episodes related to it.", inline=False)
            embed.add_field(name=f"{self.pre}pod [Name of Podcast] : [Selection Number] or {self.pre}podp [Selection No]", value="Play the podcast selection , default 0 plays the latest available episode",inline=False)
            embed.add_field(name=f"{self.pre}stop or {self.pre}dc",value="Stop and Disconnect\n Sadly Haven't Implemented any Pause for now", inline=False)
        if(podepi == None and not podname == " "):
            await ctx.send(f'Searching 🔍')
            embed = discord.Embed(colour=discord.Colour(
                0xbd10e0), description=" ")
            embed.set_thumbnail(url=self_avatar)
            embed.set_author(name=self_name, url=self_avatar,
                             icon_url=self_avatar)
            try:
                k = ph.PodSearch(podname)
            except json.JSONDecodeError:
                embed.add_field(name=f"Corrupted Feed",value="Command raised an exception: JSONDecodeError",inline=False)
                return
            except:
                embed.add_field(name=f"Somewhere Something went wrong",
                                value=r"I have 0 clue what the hell happened rn ¯\_(ツ)_/¯", inline=False)
                return
            await ctx.message.add_reaction('⏳')
            if(not k['name'] == "Podcast Not Found"):
                currentpod = ph.Podcast(k['name'], k['rss'])
                self.lastPod = currentpod
                paginationsize = ph.Pagination(k['count'],5)
                ind = 0 + 5*start
                for episode_ in currentpod.ListEpisodes()[start:start+5]:
                    embed.add_field(name=f"{ind} : "+episode_,value=k['date'],inline=False)
                    ind += 1
                if(paginationsize > 1):
                    embed.add_field(name="Change Page",value=f"```{self.pre}pod {podname} - [Page_Number]```")
                embed.set_footer(text=f"Page {start}/{paginationsize}", icon_url=self_avatar)
                try:
                    embed.set_thumbnail(url=k['image'])
                except:
                    embed.set_thumbnail(url=self_avatar)
            else:
                embed.add_field(name=f"No Podcasts Found",value="itunes returned no results",inline=False)
                embed.set_thumbnail(url=self_avatar)

        if(not podepi == None and not podname == " "):
            if(self.lastPod == None):
                k = ph.PodSearch(podname)
                currentpod = ph.Podcast(k['name'], k['rss'])
                self.lastPod = currentpod
            else:
                currentpod = self.lastPod
            await self.playPodcast(ctx,podepi=podepi,currentpod=currentpod)
            embed = discord.Embed(title=currentpod.GetEpisodeDetails(podepi)['title'],
                                  colour=discord.Colour(0xb8e986), url=currentpod.GetEpisodeDetails(podepi)['link'],
                                  description=currentpod.GetEpisodeDetails(podepi)['summary'],
                                  inline=False)

            embed.set_thumbnail(url=currentpod.PodcastImage(podepi))
            embed.set_author(name=self_name,icon_url=self_avatar)
            embed.set_footer(text=k['name'],icon_url=self_avatar)

        await ctx.send(embed=embed)

    async def playPodcast(self, context, podepi, currentpod):
        try:
            await context.voice_client.disconnect()
        except:
            pass
        if context.voice_client is None:
            if context.author.voice.channel:
                await context.author.voice.channel.connect()

        guild = context.guild
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        _source_ = currentpod.GetEpisodeMp3(podepi)
        audio_source = discord.FFmpegPCMAudio(_source_)
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)

    @commands.command(aliases=['fuckoff', 'dc' , 'disconnect'])
    async def stop(self, ctx ):
        if(ctx.author.voice.channel):
            await ctx.message.add_reaction('👍')
            embed = discord.Embed( title=f"Exiting", description=f"played" ,colour=discord.Colour(0xff5065))
            embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            embed.set_footer(text=self.client.user.name,icon_url=self.client.user.avatar_url)
            await ctx.voice_client.disconnect()
            return await ctx.reply(embed=embed)
        else:
            await ctx.message.add_reaction('❗')
            embed = discord.Embed( title=f"you are not in the voice channel", colour=discord.Colour(0xff5065))
            embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            embed.set_footer(text=self.client.user.name,icon_url=self.client.user.avatar_url)
            return await ctx.reply(embed=embed)

    @lofi.before_invoke
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice.channel:
                self.StartTime = ttime.time()
                print("timer started")
                await ctx.author.voice.channel.connect()
            else:
                embed = discord.Embed(title=f"{ctx.message.author.mention} is not connected to any Voice channel", colour=discord.Colour(0xff5065))
                embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
                embed.set_footer(text=self.client.user.name,icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)

        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
