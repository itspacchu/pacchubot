from discord.errors import DiscordException
from discord.player import AudioPlayer, AudioSource
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
    lastPod = None
    source = None
    Aplayer = None
    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(pass_context=True, aliases=['pl','plf','lf'])
    async def lofi(self, ctx,*,flavour='study'):
        voice_client: discord.VoiceClient = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        await ctx.message.add_reaction(Emotes.LOFISPARKO)
        url = ""
        flavoururls = {
            'study':'https://www.youtube.com/watch?v=5qap5aO4i9A',
            'sleep': 'https://www.youtube.com/watch?v=DWcJFNfaw9c'
        }
        async with ctx.typing():
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                info = ydl.extract_info(flavoururls[flavour], download=False)
                url = info['formats'][0]['url']
        embed = discord.Embed(title=f"Playing {flavour} + lofi", colour=discord.Colour(0xff5065), url=url)
        embed.set_image(url=f"https://i.ytimg.com/vi/{flavoururls[flavour][-11:]}/maxresdefault.jpg")
        embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=self.name, icon_url=self.avatar)
        await ctx.send(embed=embed,components=[[Button(style=ButtonStyle.red, label="Stop")],])
        await self.playmp3source(url, context=ctx)
        

    @commands.command(aliases=['podp'])
    async def podplay(self,ctx,epno=0):  
        await ctx.message.add_reaction(Emotes.PACPLAY) 
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
                try:
                    desc = currentpod.GetEpisodeDetails(podepi)['summary'][:300]
                except:
                    desc = "No Information Available"
                await self.playPodcast(ctx,podepi=podepi,currentpod=currentpod)
                embed = discord.Embed(title=currentpod.GetEpisodeDetails(podepi)['title'],colour=find_dominant_color(currentpod.PodcastImage(podepi)), url=currentpod.GetEpisodeDetails(podepi)['link'],
                                      description=desc,
                                      inline=False)
                embed.set_thumbnail(url=currentpod.PodcastImage(podepi))
                embed.set_footer(text=currentpod.GetEpisodeDetails(podepi)['title'],icon_url=self.avatar)
                await ctx.send(embed=embed, components=[[Button(style=ButtonStyle.red, label="Stop")], [Button(style=ButtonStyle.blue, label="Pause")], [Button(style=ButtonStyle.red, label="Resume")]])
            except AttributeError:
                await ctx.send("You aren't in voice channel m8")


    @commands.command(aliases=['podcast'])
    async def pod(self,ctx , * , strparse = " ",pgNo=0,searchIndex=0):        
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
            try:
                embed.set_thumbnail(url=currentpod.PodcastImage(podepi))
            except:
                pass

        del_dis = await ctx.send(embed=embed, components=[[Button(style=ButtonStyle.green, label="Play Latest"), Button(style=ButtonStyle.red, label="Prev Page"), Button(style=ButtonStyle.blue, label="Next Page"), Button(style=ButtonStyle.grey, label="Next Search Result")]])
        
        while True:
            res = await self.client.wait_for("button_click",timeout=1200)
            if(res.component.label == "Play Latest"):
                await ctx.invoke(self.client.get_command('podplay'))
            elif(res.component.label == "Next Page"):
                await del_dis.delete()
                del_dis = None
                await ctx.invoke(self.client.get_command('pod'), strparse=strparse, pgNo=pgNo+1)
            elif(res.component.label == "Prev Page" and pgNo > 2):
                await del_dis.delete()
                del_dis = None
                await ctx.invoke(self.client.get_command('pod'), strparse=strparse, pgNo=pgNo-1)
            elif(res.component.label == "Next Search Result"):
                await del_dis.delete()
                del_dis = None
                await ctx.invoke(self.client.get_command('pod'), strparse=strparse, pgNo=0 ,searchIndex=searchIndex+1)
            
            
    async def playPodcast(self, context, podepi, currentpod):
        try:
            await context.voice_client.disconnect()
        except:
            pass
        
        if context.voice_client is None:
            if context.author.voice.channel:
                await context.author.voice.channel.connect()
                
        _source_ = currentpod.GetEpisodeMp3(podepi)
        await self.playmp3source(_source_,context=context)
            
    async def playmp3source(self,mp3link:str,context):
        ctx = context
        voice_client: discord.VoiceClient = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        audio_source = discord.FFmpegPCMAudio(mp3link)
        self.source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(mp3link, before_options=ffmpeg_options), volume=100)
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            
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
            
            
            

    
    @commands.command(aliases=['pau','p'])
    async def pause(self, ctx):
        try:
            ctx.voice_client.pause()
            await ctx.message.add_reaction(Emotes.PACPAUSE)
        except:
            await ctx.send(f"> {ctx.author.mention} I see-eth nothing playin")

    @commands.command(aliases=['r'])
    async def resume(self, ctx):
        try:
            await ctx.message.add_reaction(Emotes.PACPLAY)
            ctx.voice_client.resume()
        except:
            await ctx.send(f"> {ctx.author.mention} Nothing's playing")

    
    @commands.command(aliases=['fuckoff', 'dc' , 'disconnect'])
    async def stop(self, ctx ):
        if(ctx.author.voice.channel):
            await ctx.message.add_reaction(Emotes.PACSTOP)
            await ctx.voice_client.disconnect()
            return await ctx.send(f"> {ctx.author.mention} stopped playback")
        else:
            await ctx.message.add_reaction(Emotes.PACEXCLAIM)
            return await ctx.reply("> You're not in voice channel")

    @lofi.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice.channel:
                await ctx.author.voice.channel.connect()
                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=False, self_deaf=True)
            else:
                embed = discord.Embed(title=f"> {ctx.message.author.mention} isn't in any voice channel that I can see mate", colour=discord.Colour(0xff5065))
                embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
                embed.set_footer(text=self.client.user.name,icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)

        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(MusicMixin(bot))
