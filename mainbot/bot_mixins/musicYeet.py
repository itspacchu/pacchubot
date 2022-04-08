from discord.ext import commands
import discord
import asyncio
import youtube_dl
import logging
import math
from urllib import request
import youtube_dl as ytdl
import discord
from ..__imports__ import *
from ..settings import *
from .discord_init import Discord_init_Color, DiscordInit
import html
import urllib
import pickle

YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}

def seconds_to_str(t):
    return '%02d:%02d' % divmod(t, 60)

def seconds_to_hhmmss(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def basicYTSearch(search,result_index=0):
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    search_results = re.findall(
        r"/watch\?v=(.{11})", htm_content.read().decode())
    return 'http://www.youtube.com/watch?v=' + search_results[result_index]

def basicYTPlaylist(playlist_url):
    _raw_ = None
    playlist = []
    with youtube_dl.YoutubeDL(YTDL_OPTS) as ydl:
        _raw_ = ydl.extract_info(playlist_url, download=False)
    for _ in _raw_['entries']:
        playlist.append('http://www.youtube.com/watch?v='+ _['url'])
    return playlist

# this is from my brother's bot
# https://github.com/mackdroid/bored-bot

def handle_spotify(query=None):
        if 'https://open.spotify.com/track/' in query:
            if type(query) == tuple:
                res = ''
                for i in query:
                    res += i + ' '
                query = res
            response = requests.get(query)
            filter = re.search("\"entities\":.*\"podcasts\"",response.text).group(0)[11:-11]
            response = json.loads(filter)
            song_title = html.unescape(response["items"][list(response["items"].keys())[0]]["name"])
            song_artist = html.unescape(response["items"][list(response["items"].keys())[0]]["artists"]["items"][0]["profile"]["name"])
            song_url = basicYTSearch(song_title + ' ' + song_artist)
            return [song_url,"SP"]
        else:
            return [query,"YT"]

class Video:
    """Class containing information about a particular video."""

    def __init__(self, url_or_search, requested_by,src):
        """Plays audio from (or searches for) a URL."""
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            video = self._get_info(url_or_search)
            video_format = video["formats"][0]
            self.stream_url = video_format["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.uploader = video["uploader"] if "uploader" in video else ""
            self.thumbnail = video[
                "thumbnail"] if "thumbnail" in video else None
            self.requested_by = requested_by
            self.src = src

    def _get_info(self, video_url):
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][0]["url"])  # get info for first video
            else:
                video = info
            return video

    def get_embed(self):
        """Makes an embed out of this Video's information."""
        if(self.src == "YT"):
            thiscolor = 0xff4444
        elif(self.src == "SP"):
            thiscolor = 0x44ff44

        embed = discord.Embed(
            title=self.title, description=self.uploader,colour=discord.Colour(thiscolor), url=self.video_url)
        embed.set_footer(
            text=f"Requested by {self.requested_by.name}",
            icon_url=self.requested_by.avatar_url)
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        return embed


# TODO: abstract FFMPEG options into their own file?
FFMPEG_BEFORE_OPTS = '-reconnect 1 -reconnect_streamed 1  -reconnect_delay_max 5'


async def audio_playing(ctx):
    """Checks that audio is currently playing before continuing."""
    client = ctx.guild.voice_client
    if client and client.channel and client.source:
        return True
    else:
        await ctx.send("> Not currently playing any audio.")
        raise commands.CommandError("> Not currently playing any audio.")
        


async def in_voice_channel(ctx):
    """Checks that the command sender is in the same voice channel as the bot."""
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel:
        return True
    else:
        await ctx.send("> You ain't in VC")
        raise commands.CommandError(
            "> You need to be in the channel to do that.")


async def is_audio_requester(ctx):
    return True


class Music(DiscordInit,commands.Cog):
    states = {}

    def get_state(self, guild):
        """Gets the state for `guild`, creating it if it does not exist."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    @commands.command(aliases=["stop","fuckoff","disconnect","dc"])
    @commands.guild_only()
    async def leave(self, ctx):
        await ctx.message.add_reaction(Emotes.PACSTOP)
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        if client and client.channel:
            await client.disconnect()
            state.playlist = []
            state.now_playing = None
        else:
            raise commands.CommandError("> Not in a voice channel.")

    @commands.command(aliases=["resume", "p"])
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def pause(self, ctx):
        """Pauses any currently playing audio."""
        client = ctx.guild.voice_client
        self._pause_audio(client)

    def _pause_audio(self, client):
        if client.is_paused():
            client.resume()
        else:
            client.pause()

    @commands.command(aliases=["next"])
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def skip(self, ctx):
        """Skips the currently playing song, or votes to skip it."""
        state = self.get_state(ctx.guild)
        client = ctx.guild.voice_client
        client.stop()
        await ctx.send("> Fetching from queue ...",delete_after=5.0)
        await ctx.invoke(self.client.get_command('np'))

    def _play_song(self, client, state, song,seek=0):
        append_seek_to_ffmpeg = FFMPEG_BEFORE_OPTS + f" -ss {seconds_to_hhmmss(seek)}"
        state.now_playing = song
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url, before_options=append_seek_to_ffmpeg ,options=" -preset veryfast -af bass=g=1.6:f=80:w=0.1"))

        def after_playing(err):
            if len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                self._play_song(client, state, next_song)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(),
                                                 self.client.loop)

        client.play(source, after=after_playing)

    @commands.command(aliases=["np"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def nowplaying(self, ctx):
        """Displays information about the current song."""
        state = self.get_state(ctx.guild)
        message = await ctx.send("", embed=state.now_playing.get_embed())
    


    @commands.command(aliases=["q", "playlist"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def queue(self, ctx):
        """Display the current play queue."""
        await ctx.message.add_reaction(Emotes.PACTICK)
        state = self.get_state(ctx.guild)

        embed = discord.Embed(title=f"{ctx.guild.name}'s music Queue")
        _id_ = 0
        if(len(state.playlist) > 0):
            for song in state.playlist:
                _id_ += 1
                embed.add_field(name=f"{_id_} : {song.title}", value=f"Requested by {song.requested_by.name}", inline=False)
            await ctx.send(embed=embed)
            
        else:
            await ctx.send("> Queue is empty", delete_after=5.0)

    @commands.command(aliases=["cq","removeq","rq"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def clearqueue(self, ctx):
        await ctx.message.add_reaction(Emotes.PACTICK)
        """Clears the play queue without leaving the channel."""
        state = self.get_state(ctx.guild)
        state.playlist = []
    
    @commands.command(aliases=["qs","savequeues","queuesave"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def savequeue(self, ctx, name: str):
        """Saves the current queue as a playlist."""
        if(len(name) < 0):
            await ctx.message.add_reaction(Emotes.PACNO)
            await ctx.send("> You didnt give a name ... should I save it as \"floopus dingus?\" Try again")
        else:
            queue = self.get_state(ctx.guild).playlist
            if(len(queue) == 0):
                await ctx.message.add_reaction(Emotes.PACNO)
                await ctx.send("> The queue is empty ... nothing to save")
            else:
                os.mkdir(f"{os.getcwd()}/statics/playlists/{ctx.guild.id}")
                await ctx.send("> Saving queue as \"{}\"".format(name))
                pickle.dump(queue, open(f"{os.getcwd()}/statics/playlists/{str(ctx.guild.id)}/{name}.playlist", "wb"))
                await ctx.message.add_reaction(Emotes.PACYES)

    @commands.command(aliases=["lq","loadplaylist","loadqueues"])
    @commands.guild_only()
    async def loadqueue(self, ctx, name: str):
        """Loads a playlist into the current queue."""
        await ctx.message.add_reaction(Emotes.PACNO)
        if(len(name) == 0):
            await ctx.send("> You didnt give a name ... should I load \"floopus dingus?\" (doesn't exist obviously) ")
        else:
            try:
                queue = pickle.load(open(f"{os.getcwd()}/statics/playlists/{str(ctx.guild.id)}/{name}.playlist", "rb"))
                state = self.get_state(ctx.guild)
                for song in queue:
                    state.playlist.append(song)
                await ctx.message.add_reaction(Emotes.PACYES)
                await ctx.send("> Loaded queue \"{}\"".format(name))
            except:
                await ctx.send("> Queue \"{}\" not found".format(name))

    @commands.command(aliases=["listplaylists",'listpl','listsaved'])
    @commands.guild_only()
    async def listqueues(self, ctx):
        """Lists all the saved playlists."""
        await ctx.message.add_reaction(Emotes.PACNO)
        try:
            files = os.listdir(f"{os.getcwd()}/statics/playlists/{str(ctx.guild.id)}/")
            if(len(files) == 0):
                await ctx.send("> No playlists found")
            else:
                await ctx.send("> Playlists found : ```{}```".format(files))
        except:
            await ctx.send("> No playlists found")

    @commands.command(aliases=["move","movesong"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def jumpqueue(self, ctx, song: int, new_index: int):
        await ctx.message.add_reaction(Emotes.PACTICK)
        """Moves song at an index to `new_index` in queue."""
        state = self.get_state(ctx.guild)  # get state for this guild
        if 1 <= song <= len(state.playlist) and 1 <= new_index:
            song = state.playlist.pop(song - 1)  # take song at index...
            state.playlist.insert(new_index - 1, song)  # and insert it.
            await ctx.invoke(self.client.get_command('queue'))
        else:
            await ctx.message.add_reaction(Emotes.PACNO)
            raise commands.CommandError("> Not a valid queue index")
    
    @commands.command(aliases=["delete"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def remove(self, ctx, song: int=None):
        state = self.get_state(ctx.guild) 
        if(song == None):
            await ctx.message.add_reaction(Emotes.PACTICK)
            await ctx.send("> Popping last song in queue")
            state.playlist.pop()

        elif 1 <= song <= len(state.playlist):
            await ctx.message.add_reaction(Emotes.PACTICK)
            song = state.playlist.pop(song - 1)  
            await ctx.invoke(self.client.get_command('queue'))

        else:
            await ctx.message.add_reaction(Emotes.PACNO)
            raise commands.CommandError("> I am dumb yet I know we dont have that many songs in the queue")


    @commands.command()
    @commands.guild_only()
    async def lofi(self,ctx):
        await ctx.message.add_reaction(Emotes.LOFISPARKO)
        lofi_url = "https://www.youtube.com/watch?v=5qap5aO4i9A"
        await ctx.invoke(self.client.get_command('play'), url=lofi_url)

    @commands.command(brief="Plays audio from <url>.")
    @commands.guild_only()
    async def play(self, ctx, *, url=None,showembed=True):
        if(url == None):
            url = "https://youtu.be/dQw4w9WgXcQ"
            embed=discord.Embed(color=0xc061cb)
            embed.add_field(name="p.play [ url / search / spotify url ]  ", value="```-loop number``` to loop the song", inline=False)
            embed.add_field(name="p.play <>  -loop number", value="loops the song in queue", inline=False)
            embed.add_field(name="p.queue", value="shows the current queue", inline=False)
            embed.add_field(name="p.move [ from ] [ to ]", value="moves song index : from → to", inline=False)
            embed.add_field(name="p.remove [ index ]", value="removes the last song by default ", inline=False)
            embed.add_field(name="p.nowplaying / p.np", value="shows now playing song", inline=False)
            embed.add_field(name="p.clearqueue / p.cq", value="clears the queue", inline=False)
            embed.add_field(name="p.lofi", value="plays lofigirl's lofi stream", inline=False)
            embed.add_field(name="p.pod", value="Show Podcast help section", inline=True)
            embed.set_footer(text="nub now get rollllled :D")
            await ctx.send(embed=embed)


        url_split = url.split("loop")
        try:
            loopcount = int(url_split[1])
        except:
            loopcount = 0

        url = url_split[0]
    
        if(loopcount > 0):
            await ctx.send("> looping the song".format(loopcount))
            progbar = await ctx.send("```[==========] 0%```")
            for i in range(int(loopcount)):
                prog = int((i/loopcount)*100)
                await progbar.edit(content=f"```[{'#'*int(prog/10)} {'='*int(10-(prog/10))}] {prog}%```")
                await ctx.invoke(self.client.get_command('play'), url=url,showembed=False)
            await progbar.edit(content=f"```[{'#'*10}] Done```")
            return
        try:
            if("/playlist?list=" in url):
                await ctx.send("> Parsing playlists",delete_after=5.0)
                ytplaylist = basicYTPlaylist(url)
                progbar = await ctx.send("```[==========] 0%```")
                i=0
                for song in ytplaylist: 
                    tot = len(ytplaylist)
                    prog = int((i/tot)*100)
                    i+=1
                    await progbar.edit(content=f"```[{'#'*int(prog/10)} {'='*int(10-(prog/10))}] {prog}%```")
                    await ctx.invoke(self.client.get_command('play'),url=song,showembed=False)
                await ctx.send("> Added {} songs to queue".format(len(ytplaylist)))
                await progbar.edit(content=f"``` [{'#'*10}] Done```")
                return
        except Exception as e:
            await ctx.send(f"> Something somewhere went wrong \n ||{e}||",delete_after=5.0)
            return

        try:
            timegx = r"[\?&]t=\d*"
            seekamt = int(re.findall(timegx,url)[0][1:].replace("t=",''))
            await ctx.send(f"> Seeking based on url {seconds_to_hhmmss(seekamt)} hours")
        except IndexError:
            seekamt = 0

        url,whrc = handle_spotify(url)
        if(whrc == "SP"):
            await ctx.send("> Fetching from spotify",delete_after=5.0)
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)  # get the guild's state

        if client and client.channel:
            try:
                video = Video(url, ctx.author , src=whrc)
            except youtube_dl.DownloadError as e:
                logging.warn(f"Error downloading video: {e}")
                await ctx.send("> Something went wrong in getting the video")
                return
            
            await ctx.message.add_reaction(Emotes.PACPLAY)
            state.playlist.append(video)
            if(showembed):
                message = await ctx.send("> Added to queue", embed=video.get_embed())
        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                try:
                    video = Video(url, ctx.author,whrc)
                except youtube_dl.DownloadError as e:
                    await ctx.send("> Something went wrong!! \n```{e}```")
                    return
                client = await channel.connect()
                self._play_song(client, state, video, seekamt)
                await ctx.message.add_reaction(Emotes.PACPLAY)
                message = await ctx.send("", embed=video.get_embed(),components=[Button(style=ButtonStyle.URL, label="Youtube",url=video.video_url)])
                logging.info(f"Now playing '{video.title}'")
            else:
                await ctx.message.add_reaction(Emotes.PACNO)
                raise commands.CommandError(
                    "> I might be your music bot but I can't get your lazy ass to join voice channel :/")

    @commands.check(audio_playing)
    @commands.guild_only()               
    @commands.command(aliases=['pau'])
    async def pause(self, ctx):
        try:
            ctx.voice_client.pause()
            await ctx.message.add_reaction(Emotes.PACPAUSE)
            await asyncio.sleep(10)
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction(Emotes.PACNO)
            await ctx.send(f"> {ctx.author.mention} wait .. I'm playing something??")

    @commands.guild_only()
    @commands.command(aliases=['res'])
    async def resume(self, ctx):
        try:
            await ctx.message.add_reaction(Emotes.PACPLAY)
            ctx.voice_client.resume()
            await asyncio.sleep(10)
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction(Emotes.PACNO)
            await ctx.send(f"> {ctx.author.mention} .. I dont remember pausing..? Something playing??")
    
    @commands.command(aliases=['getmp3','mp3'])
    async def download_song(self,ctx,*,query=None):
        downloadl = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        }
        if(query == None):
            state = self.get_state(ctx.guild).now_playing
            query = state.video_url

        url = "Not Found"
        with youtube_dl.YoutubeDL(downloadl) as ydl:
            info = ydl.extract_info(query, download=False)
            url = info['formats'][0]['url']
        if(url != "Not Found"):
            try:
                await ctx.reply(Emotes.PACTICK,components=[Button(style=ButtonStyle.URL, label="Download",url=url)])
            except Exception as e:
                await ctx.send(f"**Download** : {url} \n Some Error Occurred while processing || {e} ||")
        else:
            await ctx.reply("> Not Found" , delete_after=3.0)




class GuildState:
    """Helper class managing per-guild state."""

    def __init__(self):
        self.playlist = []
        self.now_playing = None

    def is_requester(self, user):
        return self.now_playing.requested_by == user


def setup(bot):
    bot.add_cog(Music(bot))
