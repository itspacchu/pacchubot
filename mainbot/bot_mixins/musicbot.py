from discord.errors import DiscordException
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
        await ctx.send("> Disabled")
        return
        await ctx.message.add_reaction('🎧') 
        if ("youtube.com" in str(url) or "youtu.be"):
            async with ctx.typing():
                player = await YTDLSource.from_url(url=url, loop=self.client.loop, stream=True)
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
                player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
                ctx.voice_client.play(player, after=None)

        embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=self.name, icon_url=self.avatar)
        await ctx.reply(embed=embed)

    @commands.command(pass_context=True, aliases=['pl'])
    async def lofi(self, ctx, *, url="https://youtu.be/5qap5aO4i9A"):
        await ctx.send("> Disabled")
        return
        async with ctx.typing():
            player = await YTDLSource.from_url(self,url=url, loop=self.client.loop, stream=True)
            ctx.voice_client.play(player, after=None)
            embed = discord.Embed(title="Playing from Youtube", colour=discord.Colour(0xff5065), url=url, description=player.title)
            embed.set_image(url="https://i.ytimg.com/vi/5qap5aO4i9A/maxresdefault.jpg")
        embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=self.name, icon_url=self.avatar)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['oldpodp','podp'])
    async def podplay(self,ctx,epno=0):    
        podepi = epno
        if(self.lastPod == None):
            embed = discord.Embed(colour=discord.Colour(0xbd10e0), description=" ")
            embed.set_thumbnail(url=self.avatar)
            embed.set_author(name=self.name, url=self.avatar,icon_url=self.avatar)
            embed.add_field(name=f"No Recent Podcast Searches",value=f"search for podcast using {self.pre}pod",inline=False)
            embed.set_thumbnail(url=self.avatar)
            await ctx.send(embed=embed)
        else:
            currentpod = self.lastPod
            try:
                await self.playPodcast(ctx,podepi=podepi,currentpod=currentpod)
                embed = discord.Embed(title=currentpod.GetEpisodeDetails(podepi)['title'],
                                      colour=find_dominant_color(currentpod.PodcastImage(podepi)), url=currentpod.GetEpisodeDetails(podepi)['link'],
                                      description=currentpod.GetEpisodeDetails(podepi)['summary'][:300],
                                      inline=False)
                embed.set_thumbnail(url=currentpod.PodcastImage(podepi))
                embed.set_author(name=self.name,icon_url=self.avatar)
                embed.set_footer(text=currentpod.GetEpisodeDetails(podepi)['title'],icon_url=self.avatar)
                await ctx.send(embed=embed, components=[[Button(style=ButtonStyle.red, label="Stop")],])
            except AttributeError:
                await ctx.send("You aren't in voice channel m8")
        while True:
            res = await self.client.wait_for("button_click")
            if(await ButtonProcessor(ctx,res,"stop")):
                await ctx.invoke(self.client.get_command('stop'))
                break

    @commands.command(aliases=['oldpodcast','podcast'])
    async def pod(self,ctx , * , strparse = " ",pgNo=0,searchIndex=0):    
        await ctx.message.add_reaction('❕')  
    
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
            start = pgNo
            podname = podname_.split('-')[0]
        except:
            start = 0
            podname = podname_
        if(podname == " "):
            embed = discord.Embed(colour=discord.Colour(0x91ff), description="Podcast Section")
            embed.set_thumbnail(url=self.avatar)
            embed.set_author(name=self.name, icon_url=self.avatar)
            embed.add_field(name=f"{self.pre}pod", value="This very command you ran",inline=False)
            embed.add_field(name=f"{self.pre}pod [Name of Podcast]",value="Searches for the Podcast and shows Episodes related to it.", inline=False)
            embed.add_field(name=f"{self.pre}pod [Name of Podcast] : [Selection Number] or {self.pre}podp [Selection No]", value="Play the podcast selection , default 0 plays the latest available episode",inline=False)
            embed.add_field(name=f"{self.pre}stop or {self.pre}dc",value="Stop and Disconnect\n Sadly Haven't Implemented any Pause for now", inline=False)
        if(podepi == None and not podname == " "):
            await ctx.message.add_reaction('🔍') 
            try:
                k = ph.PodSearch(podname,searchIndex=searchIndex)
            except json.JSONDecodeError as e:
                embed = discord.Embed(colour=discord.Colour(0x120012), description=" ")
                embed.set_thumbnail(url=self.avatar)
                embed.set_author(name=self.name, url=self.avatar,icon_url=self.avatar)
                embed.add_field(name=f"Corrupted Feed",value=e,inline=False)
                return
            except:
                embed = discord.Embed(colour=discord.Colour(0x120012), description=" ")
                embed.set_thumbnail(url=self.avatar)
                embed.set_author(name=self.name, url=self.avatar, icon_url=self.avatar)
                embed.add_field(name=f"Somewhere Something went wrong",value=r"I have 0 clue what the hell happened rn ¯\_(ツ)_/¯", inline=False)
                return
            await ctx.message.add_reaction('⏳')
            if(not k['name'] == "Podcast Not Found"):
                currentpod = ph.Podcast(k['name'], k['rss'])
                self.lastPod = currentpod
                paginationsize = ph.Pagination(k['count'],5)
                try:
                    thiscol = find_dominant_color(k['image'])
                except:
                    thiscol = 0xffffff
                embed = discord.Embed(colour=thiscol, description=" ")
                embed.set_thumbnail(url=self.avatar)
                embed.set_author(name=self.name, url=self.avatar, icon_url=self.avatar)
                ind = 0 + 5*start
                for episode_ in currentpod.ListEpisodes()[start:start+5]:
                    embed.add_field(name=f"{ind} : "+episode_,value=k['date'],inline=False)
                    ind += 1
                embed.set_footer(text=f"Page {start+1}/{paginationsize}", icon_url=self.avatar)
                try:
                    embed.set_thumbnail(url=k['image'])
                except:
                    embed.set_thumbnail(url=self.avatar)
            else:
                embed = discord.Embed(colour=discord.Colour(0x120012), description=" ")
                embed.set_thumbnail(url=self.avatar)
                embed.add_field(name=f"No Podcasts Found",value="No Results",inline=False)
                embed.set_thumbnail(url=self.avatar)

            embed.set_thumbnail(url=currentpod.PodcastImage(podepi))

        del_dis = await ctx.send(embed=embed, components=[[Button(style=ButtonStyle.green, label="Play Latest"), Button(style=ButtonStyle.red, label="Prev Page"), Button(style=ButtonStyle.blue, label="Next Page"), Button(style=ButtonStyle.grey, label="Next Search Result")]])
        
        res = await self.client.wait_for("button_click")
        if(res.component.label == "Play Latest"):
            await del_dis.delete()
            await ctx.invoke(self.client.get_command('podplay'))
        elif(res.component.label == "Next Page"):
            await del_dis.delete()
            await ctx.invoke(self.client.get_command('pod'), strparse=strparse, pgNo=pgNo+1)
        elif(res.component.label == "Prev Page" and pgNo > 2):
            await del_dis.delete()
            await ctx.invoke(self.client.get_command('pod'), strparse=strparse, pgNo=pgNo-1)
        elif(res.component.label == "Next Search Result"):
            await del_dis.delete()
            await ctx.invoke(self.client.get_command('pod'), strparse=strparse, pgNo=0 ,searchIndex=searchIndex+1)
            


    async def playPodcast(self, context, podepi, currentpod):
        try:
            await context.voice_client.disconnect()
        except:
            pass
        if context.voice_client is None:
            if context.author.voice.channel:
                await context.author.voice.channel.connect()

        guild = context.guild
        voice_client: discord.VoiceClient = discord.utils.get(self.client.voice_clients, guild=guild)
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
        await ctx.message.add_reaction('❕')
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

def setup(bot):
    bot.add_cog(MusicMixin(bot))
