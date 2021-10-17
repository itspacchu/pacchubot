from operator import ne
from nextcord.activity import Spotify
from nextcord.channel import VoiceChannel
import spotipy
from imports import *
import urllib
from nextcord.player import AudioPlayer,AudioSource
from nextcord import embeds,FFmpegOpusAudio
from youtube_dl import YoutubeDL
import re
from ctypes.util import find_library
from apihandler import spotify_handler
from podcasthandler import Podcast,PodResults,PodSearch,PodcastEpisode


class MusicPlaybackSource:
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    PLAYER_PROXY = None

    def __init__(self,query=None,podcast:PodcastEpisode=None,podcast_epi=0):
        if("mp3" in query and "http" in query):
            self.handle_raw_mp3_playback(podcast)
        if(podcast):
            self.handle_podcast(podcast)
        else:
            self.handle_music(query)
    
    def handle_raw_mp3_playback(self,query:str):
        self.PLAYER_PROXY = {
                "src": "RAWMP3",
                "url":query,
                "query":query,
                "title":"RAW MP3 PLAYBACK",
                "description":"Streaming RAW MP3",
                "duration":"0",
                "thumbnail":"https://logosandtypes.com/wp-content/uploads/2020/08/walkman.svg",
                "uploader":"God Knows where you yeeted this from",
                "uploader_url":query  
            }

    def handle_podcast(self,podcast:PodcastEpisode):
        self.PLAYER_PROXY = {
            "src": "PodcastEpisode",
            "url":podcast.GetEpisodeMp3(),
            "query":podcast.GetItunes(),
            "title":podcast.name,
            "description":podcast.GetEpisodeDescription(),
            "duration":podcast.GetEpisodeDuration(),
            "thumbnail":podcast.GetEpisodeImage(),
            "uploader":podcast.GetPodcast(),
            "uploader_url":podcast.GetItunes()
        }
        return self.PLAYER_PROXY


    def handle_music(self,query=None):
        bboost = False
        if(query == None or query == "RR"):
            self.PLAYER_PROXY = {
                "src": "None",
                "url":"https://s3-us-west-2.amazonaws.com/true-commitment/01-NeverGonnaGiveYouUp.mp3",
                "query":"https://s3-us-west-2.amazonaws.com/true-commitment/01-NeverGonnaGiveYouUp.mp3",
                "title":"Hmm someone forgot to set a url",
                "description":"Usage : play [Youtube URL / Youtube search / Spotify URL]",
                "duration":"69",
                "thumbnail":"https://c.tenor.com/u9XnPveDa9AAAAAM/rick-rickroll.gif",
                "uploader":"Rick Ashley",
                "uploader_url":"https://s3-us-west-2.amazonaws.com/true-commitment/01-NeverGonnaGiveYouUp.mp3"  
            }
            return self.PLAYER_PROXY
        
        src = "url"
        if('https://open.spotify.com/track/' in query):
            spotiurl = query
            song_stuff = spotify_handler.track("spotify:" + spotiurl[25:spotiurl.find('?')].replace("/",":"))
            query = self.basicYTSearch(song_stuff['artists'][0]['name'] + " " + song_stuff['name'])
            src = "Spotify"
        
        elif('https://youtube' not in query):
            query = self.basicYTSearch(query)
            src = "Youtube"
        
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)

        self.PLAYER_PROXY = {
            "src": src,
            "url":info['url'],
            "query":query,
            "title":info['title'],
            "description":info['description'][:240] + "...",
            "duration":info['duration'],
            "thumbnail":info['thumbnails'][-1]['url'],
            "uploader":info['uploader'],
            "uploader_url":info['uploader_url']
        }
        return self.PLAYER_PROXY

            
    def basicYTSearch(self, search):
        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string)
        search_results = re.findall(
            r"/watch\?v=(.{11})", htm_content.read().decode())
        return 'http://www.youtube.com/watch?v=' + search_results[0]



class MusicCore(commands.Cog):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    client = None
    AUDIO_QUEUE = {}
    SERVER_FFMPEG_OPTN = {}
    PODSEARCH = {}
    SERVER_PLAYBACK_TIME = {}

    
    def __init__(self, client):
        self.client = client
    
    def create_pod_episode_embed(self,pod:PodcastEpisode):
        embed = nextcord.Embed(title=pod.name + ' ' + pod.GetEpisodeTitle(), description=pod.GetEpisodeDescription(),url=pod.GetItunes(), color=0x1DB954)
        embed.set_thumbnail(url=pod.GetEpisodeImage())
        embed.add_field(name="Author", value=pod.name)
        return embed

    def create_pod_embed(self,pod:Podcast):
        FeedDetails = pod.GetFeedDetails()
        embed = nextcord.Embed(title=FeedDetails['name'], description=FeedDetails['content'],url=FeedDetails['link'], color=0x1DB954)
        embed.set_thumbnail(url=FeedDetails['image'])
        embed.add_field(name="Author", value=FeedDetails['author'])
        embed.add_field(name="tags", value=",".join(FeedDetails['tags']))
        embed.set_author(name=FeedDetails['author'],value=FeedDetails['image'])
        return embed

    def create_embed(self,mps:dict):
        if(mps['src'] == "Youtube"):
            color = 0xFF0000
        elif(mps['src'] == "Spotify"):
            color = 0x1DB954
        else:
            color = 0xFFFFFF
        embed = nextcord.Embed(title=mps['title'], description="```" + mps['description'] + "```",url=mps['query'] , color=color)
        embed.set_thumbnail(url=mps['thumbnail'])
        embed.set_author(name=mps['uploader'], url=mps['uploader_url'])
        return embed

    @commands.command()
    async def join(self, ctx, *, channel: nextcord.VoiceChannel=None):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        if(channel == None):
            channel = ctx.author.voice.channel
        self.AUDIO_QUEUE[ctx.guild.id] = [] #empty queue
        await channel.connect()
    
    @commands.command(aliases=['rb','reseteq'])
    async def remove_bass(self, ctx):
        self.SERVER_FFMPEG_OPTN[ctx.guild.id] = self.FFMPEG_OPTIONS
        await ctx.message.add_reaction(Emotes.PACTICK)
    
    @commands.command(aliases=['ab','bassboost'])
    async def add_bass(self, ctx, bass_gain:int=8 , bass_freq:float=72.0,bass_q:float=1.2):
        current_ffmpeg = self.FFMPEG_OPTIONS.copy()
        current_ffmpeg['options'] += f" -af bass=g={bass_gain}:f={bass_freq}:w={bass_q}"
        await ctx.send(f"> EQ is enabled \n```bass : {bass_gain}dB\nfreq : {bass_freq}Hz\nq_fac : {bass_q}```")

        if(bass_gain > 8):
            await ctx.send(f"> [Warning] : Bass gain is too high can cause clipping, Rip Ears\n",delete_after=5)
        if(bass_q < 1.0):
            await ctx.send(f"> [Warning] : Quality Factor too narrow, it will cause Resonance, Annoying!!",delete_after=5)

        self.SERVER_FFMPEG_OPTN[ctx.guild.id] = current_ffmpeg
        await ctx.message.add_reaction(Emotes.PACTICK)

    async def bass_booster(self,ctx,query):
        try:
            if('-b' in query):
                query = query.replace('-b','')
                current_ffmpeg = self.FFMPEG_OPTIONS.copy()
                current_ffmpeg['options'] += " -af bass=g=8:f=75:w=1.2"
                await ctx.send(f"> EQ is enabled ```bass : 8dB```")
                self.SERVER_FFMPEG_OPTN[ctx.guild.id] = current_ffmpeg
            else:
                current_ffmpeg = self.FFMPEG_OPTIONS
        except:
            current_ffmpeg = self.FFMPEG_OPTIONS
        return current_ffmpeg
    
    @commands.command()
    async def reprqueue(self, ctx):
        await ctx.send(f"{self.AUDIO_QUEUE[ctx.guild.id][0]}")
    
    @commands.command(aliases=['dc','fuckoff','stop','leave'])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction(Emotes.PACTICK)
        self.AUDIO_QUEUE[ctx.guild.id] = []

    @commands.command(aliases=['aq','addq'])
    async def addqueue(self, ctx, *, query: str):
        try:
            self.AUDIO_QUEUE[ctx.guild.id].append(MusicPlaybackSource(query).PLAYER_PROXY)
            player = self.AUDIO_QUEUE[ctx.guild.id][-1]
            await ctx.message.add_reaction(Emotes.PACTICK)
            await ctx.send(f"Added to queue: {player['title']}")
        except KeyError:
            await ctx.send("> Nothing's playing m8")
    
    @commands.command(aliases=['dq','delq'])
    async def delqueue(self, ctx, query:int):
        if(query > len(self.AUDIO_QUEUE[ctx.guild.id])):
            await ctx.send("> Index out of range")
            return
        await ctx.message.add_reaction(Emotes.PACTICK)
        await ctx.send(f"> Removing {self.AUDIO_QUEUE[ctx.guild.id].pop(query)['title']}")
        self.AUDIO_QUEUE[ctx.guild.id].pop(query)
        
    
    @commands.command(aliases=['sq','q'])
    async def queue(self, ctx):
        if(len(self.AUDIO_QUEUE[ctx.guild.id]) == 0):
            await ctx.send("> Queue is empty")
            return
        queuegen = ""
        for i in range(len(self.AUDIO_QUEUE[ctx.guild.id])):
            queuegen += f"[{i+1}] - {self.AUDIO_QUEUE[ctx.guild.id][i]['title']}"
            if(i == 0):
                queuegen += " ⟵ Now playing "
            queuegen += "\n\n"

        embed = nextcord.Embed(title=f"{ctx.guild.name}'s Moosik", description="```" + queuegen + "```", color=0x800080)
        await ctx.send(embed=embed)

    async def clear_audio_src(self,player):
        await player.cleanup()
        

    async def on_player_finished(self,ctx):
        self.AUDIO_QUEUE[ctx.guild.id].pop(0)
        if(len(self.AUDIO_QUEUE[ctx.guild.id]) > 0):
            try:
                ffmpeg_optns = self.SERVER_FFMPEG_OPTN[ctx.guild.id]
            except KeyError:
                ffmpeg_optns = self.FFMPEG_OPTIONS
            player = FFmpegOpusAudio(self.AUDIO_QUEUE[ctx.guild.id][0]["url"],**ffmpeg_optns)
            await ctx.send(f"> Now playing: {self.AUDIO_QUEUE[ctx.guild.id][0]['title']}")
            await ctx.voice_client.play(player)
            await asyncio.sleep(self.AUDIO_QUEUE[ctx.guild.id][0]['duration']+1)
        else:
            await ctx.voice_client.stop()
            await ctx.send("> Queue is empty")

    @commands.command(aliases=['next'])
    async def skip(self, ctx):
        try:
            if(len(self.AUDIO_QUEUE[ctx.guild.id]) == 0):
                await ctx.send("> Queue is empty")
                return
            await asyncio.sleep(1) 
            nextcord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
            await ctx.message.add_reaction(Emotes.PACPLAY)
            await self.on_player_finished(ctx)
        except IndexError as e:
            await ctx.send(f"> {e} Something went wrong!")
        

    @commands.command(name="Play youtube source",aliases=['play'])
    async def play_src(self,ctx,*,query=None):
        current_ffmpeg = await self.bass_booster(ctx,query)
        await ctx.message.add_reaction(Emotes.PACPLAY)
        source = MusicPlaybackSource(query).PLAYER_PROXY
        player = FFmpegOpusAudio(source["url"],**self.SERVER_FFMPEG_OPTN[ctx.guild.id])
        voice = ctx.voice_client
        if(voice == None):
            await ctx.invoke(self.join)
            voice = ctx.voice_client
        self.AUDIO_QUEUE[ctx.guild.id].append(source)
        if(len(self.AUDIO_QUEUE[ctx.guild.id]) >= 1):
            await ctx.send(embed=self.create_embed(source))
            await voice.play(player)
            await asyncio.sleep(source["duration"] + 1)
            await self.on_player_finished(ctx)


    @commands.command(aliases=['podsearch'])
    async def podcasthandling(self, ctx, *, query: str):
        SearchPod = PodSearch(query)
        await ctx.send(embed=self.create_pod_embed(SearchPod))
        self.PODSEARCH[ctx.guild.id] = SearchPod
        self.PODSEARCH[ctx.guild.id]['search_id'] = 0
        self.PODSEARCH[ctx.guild.id]['query'] = query
    
    @commands.command()
    async def podnext(self, ctx):
        SearchPod = PodSearch(self.PODSEARCH[ctx.guild.id]['query'],self.PODSEARCH[ctx.guild.id]['search_id']+1)
        await ctx.send(embed=self.create_pod_embed(SearchPod))
        self.PODSEARCH[ctx.guild.id] = SearchPod
        self.PODSEARCH[ctx.guild.id]['search_id'] += 1
    
    @commands.command()
    async def podprev(self, ctx):
        SearchPod = PodSearch(self.PODSEARCH[ctx.guild.id]['query'],self.PODSEARCH[ctx.guild.id]['search_id']-1)
        await ctx.send(embed=self.create_pod_embed(SearchPod))
        self.PODSEARCH[ctx.guild.id] = SearchPod
        if(self.PODSEARCH[ctx.guild.id]['search_id'] == 0):
            pass
        else:
            self.PODSEARCH[ctx.guild.id]['search_id'] -= 1
    
    @commands.command(aliases=['podepi'])
    async def podsearchEpisode(self,ctx,*,query):
        MyEpisode = PodcastEpisode(query)
        try:
            self.PODSEARCH[ctx.guild.id]['episode'] = MyEpisode
        except KeyError:
            self.PODSEARCH[ctx.guild.id] = {}
            self.PODSEARCH[ctx.guild.id]['episode'] = MyEpisode
        await ctx.send(embed=self.create_pod_episode_embed(MyEpisode))
    

    @commands.command(aliases=['pod2queue'])
    async def addPodcastToQueue(self,ctx,*,query=None):
        if(query == None):
            await ctx.send("> Please enter a query")
            return
        MyEpisode = PodcastEpisode(query)
        self.AUDIO_QUEUE[ctx.guild.id].append(MyEpisode)
        await ctx.send(embed=self.create_pod_episode_embed(MyEpisode))
        self.PODSEARCH[ctx.guild.id] = MyEpisode
        self.PODSEARCH[ctx.guild.id]['search_id'] = 0
        self.PODSEARCH[ctx.guild.id]['query'] = query


    @commands.command(aliases=['podplay'])
    async def podplayepisode(self,ctx,*,query=None):
        try:
            if(query is not None):
                raise KeyError("No Podcasts found")
            MyEpisode = self.PODSEARCH[ctx.guild.id]['episode']
        except KeyError:
            MyEpisode = PodcastEpisode(query)
        current_ffmpeg = await self.bass_booster(ctx,query)
        await ctx.message.add_reaction(Emotes.PACPLAY)
        source = MusicPlaybackSource(podcast=MyEpisode).PLAYER_PROXY
        player = FFmpegOpusAudio(source["url"],**self.SERVER_FFMPEG_OPTN[ctx.guild.id])
        voice = ctx.voice_client
        if(voice == None):
            await ctx.invoke(self.join)
            voice = ctx.voice_client
        self.AUDIO_QUEUE[ctx.guild.id].append(source)
        if(len(self.AUDIO_QUEUE[ctx.guild.id]) >= 1):
            await ctx.send(embed=self.create_pod_episode_embed(MyEpisode))
            await voice.play(player)
            await asyncio.sleep(source["duration"] + 1)
            await self.on_player_finished(ctx)

    @commands.command(name="replay",aliases=['loop'])
    async def loop(self,ctx):
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction(Emotes.PACTICK)
        await ctx.send(f"> Loop is now {'on' if ctx.voice_state.loop else 'off'}")
        

    @commands.command()
    async def pause(self,ctx):
        voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.message.add_reaction(Emotes.PACPAUSE)
            voice.pause()
        else:
            await ctx.message.add_reaction(Emotes.PACEXCLAIM)
            await ctx.send("Currently no audio in playing")

    @commands.command()
    async def resume(self,ctx):
        voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            await ctx.message.add_reaction(Emotes.PACPLAY)
            voice.resume()
        else:
            await ctx.message.add_reaction(Emotes.PACEXCLAIM)
            await ctx.send("The audio is not paused.")


    @podplayepisode.before_invoke
    @play_src.before_invoke
    async def ensure_voice(self,ctx):
        if(ctx.voice_client is None):
            if(ctx.author.voice.channel != None):
                self.AUDIO_QUEUE[ctx.guild.id] = [] #empty queue
                await ctx.author.voice.channel.connect()
                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=False, self_deaf=True)
            else:
                embed = Embed(title=f"> {ctx.message.author.mention} isn't in any voice channel that I can see mate", colour=nextcord.Colour(0xff5065))
                embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar.url)
                await ctx.send(embed=embed)
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        
    
            
