from .__imports__ import *
from .settings import *


# File Imports
perks = json.load(jsonfile)


# Mongo DB Content
db = mongo_client['PacchuSlave']
serverstat = db['serverstat']
bruhs = db['bruh']
animeSearch = db['animeSearch']
charSearch = db['charSearch']
animePics = db['animePics']
mangaSearch = db['mangaSearch']
gptDb = db['gptQuery']
PodcastSuggest = db['PodSuggest']
VoiceUsage = db['VoiceActivity']


# Discord bot
client = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())
client.remove_command('help')
# slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    self_name = client.user
    self_avatar = client.user.avatar_url
    statustxt = "Questioning Everything now 🧠"
    activity = discord.Game(name=statustxt)
    if(client):
        print("Connected to Database")
    print(db.list_collection_names())
    await client.change_presence(status=discord.Status.online, activity=activity)



@client.command(aliases=['h', 'halp' , 'hel'])
async def help(ctx):
    embed = discord.Embed(color=0xae00ff, description=f"Created by Pacchu")
    embed.set_author(name=self_name, icon_url=self_avatar)
    embed.set_thumbnail(url=self_avatar)
    embed.add_field(name=f"{command_prefix}perk",value="Cool awesome stuff in this", inline=False)
    embed.add_field(name=f"{command_prefix}anime/ani",value="Searches for given anime", inline=True)
    embed.add_field(name=f"{command_prefix}manga/m",value="Searches for give Manga", inline=True)
    embed.add_field(name=f"{command_prefix}anichar/ac",value="Searches for given Anime Charactor ", inline=True)
    embed.add_field(name=f"{command_prefix}anipics/ap",value="Searches for Images of given Anime Charactor", inline=True)
    embed.add_field(name=f"{command_prefix}stats",value="partially implemented **bugs**", inline=False)
    embed.add_field(name=f"{command_prefix}pod",value="Podcast playback section", inline=False)
    embed.add_field(name=f"{command_prefix}play/p  , {command_prefix}lofi/pl",value="Youtube Playback and Lofi music", inline=False)
    embed.add_field(name=f"{command_prefix}invite",value="Invite link for this bot", inline=False)
    embed.add_field(name=f"{command_prefix}help",value="isnt it obvious :o", inline=False)
    embed.set_footer(text=f"{self_name} {version}", icon_url=self_avatar)
    try:
        await ctx.reply(embed=embed)
    except AttributeError:
        await ctx.send(embed=embed)

@client.command(aliases=['per', 'perks'])
async def perk(ctx):
    embed = discord.Embed(title=client.user.name.title(),description=f"{self_name} Perks", color=0xff9500)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name=f"{command_prefix}avatar @Pacchu / {command_prefix}av @Pacchu",value=f"Something of use atleast", inline=False)
    embed.add_field(name=f"{command_prefix}bruh [emote,link,text message]",value=f"Something to be saved? idk why it an option", inline=False)
    embed.add_field(name=f"{command_prefix}gpt \"Today is a wonderful..\"",value="gpt neo text completion", inline=True)
    embed.add_field(name=f"{command_prefix}q \"Why is chocolate beautiful?\"",value="gpt neo answering", inline=True)
    embed.add_field(name=f"{command_prefix}spotify @mention",value="Gets the user's Spotify activity", inline=False)

    embed.add_field(name=f"{command_prefix}kill @mention",value=f"Kills the user ... well not really", inline=True)
    embed.add_field(name=f"{command_prefix}kiss @mention",value=f"kiss?", inline=True)
    embed.add_field(name=f"{command_prefix}hug @mention",value=f"Hugs the user?", inline=True)

    embed.set_footer(text=f" {client.user.name} {version}",icon_url=client.user.avatar_url)
    await ctx.reply(embed=embed)

@client.command(aliases=['av', 'pic' , 'dp'])
async def avatar(ctx, member: discord.Member = None):
    hgp = member
    await ctx.message.add_reaction('🙄')
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(title="OwO", description=f"{ctx.message.author.mention} steals ...wait thats your OWN", colour=discord.Colour(0xa06a6a))
        embed.set_image(url=ctx.message.author.avatar_url)
    else:
        embed = discord.Embed(title="Swong..!", description=f"{ctx.message.author.mention} yeets {hgp.mention}'s profile pic 👀'", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=hgp.avatar_url)
    try:
        embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    except:
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text=f"{client.user.name}",icon_url=client.user.avatar_url)
    await ctx.reply(embed=embed)

@client.command(aliases=['achar', 'ac'])
async def anichar(ctx, *Query):
    global ani
    animeQuery = queryToName(Query)
    try:
        await ctx.message.add_reaction('🔍')
        asrc = ani.character(ani.search('character', str(animeQuery))['results'][0]['mal_id'])
        if(len(asrc['about']) < 511):
            embed = discord.Embed(title=f"**{asrc['name']}**", colour=discord.Colour(0xa779ff), url=asrc['url'], description=asrc['about'].strip().replace(r'\n', '')+'...')
        else:
            embed = discord.Embed(title=f"**{asrc['name']}**", colour=discord.Colour(0xa779ff), url=asrc['url'], description=asrc['about'][512].strip().replace(r'\n', '')+'...')
        embed.set_image(url=asrc['image_url'])
        embed.set_footer(text=f"Not the correct Character ... Try spelling their full name", icon_url=client.user.avatar_url)
        embed.add_field(name="Waifu Vote", value=f"{asrc['member_favorites']} have liked them", inline=False)
        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.send(embed=embed)
        try:
            dbStore = {
                "charname":animeQuery,
                "username": ctx.message.author.name,
                "guild":ctx.message.guild.id
            }
        except AttributeError:
            dbStore = {
                "charname": animeQuery,
                "username": ctx.message.author.name,
                "guild": "DirectMessage"
            }
        charSearch.insert_one(dbStore)
    except:
        await ctx.message.add_reaction('😞')
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Character Not Found",value="That Character is not found ", inline=False)
        embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.send(embed=embed)

@client.command(aliases=['ap', 'anip' ,'anishow'])
async def anipics(ctx, *Query):
    global  ani, http
    charQuery = queryToName(Query)
    try:
        await ctx.message.add_reaction('🔍')
        charid = ani.search('character', charQuery)['results'][0]
        url = f"https://api.jikan.moe/v3/character/{charid['mal_id']}/pictures"
        picdat = json.loads(http.request('GET', url).data.decode())['pictures']
        embed = discord.Embed(title=f"**{charid['name']}**", colour=discord.Colour(0xa779ff), url=charid['url'])
        embed.set_image(url=choice(picdat)['small'])
        embed.set_footer(text=f"Not the correct charector... Try spelling their full name", icon_url=client.user.avatar_url)
        await ctx.reply(embed=embed)
        dbStore = {
            "charname":charQuery,
            "username": ctx.message.author.name,
        }
        animePics.insert_one(dbStore)
    except:
        await ctx.message.add_reaction('😞')
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Images Not Found",value=" Coudn't find any images on given Query ", inline=False)
        embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
        await ctx.reply(embed=embed)

@client.command(aliases=['ani', 'anim'])
async def anime(ctx, *Query):
    global  ani
    animeQuery = queryToName(Query)
    dbStore = {
        "charname": animeQuery,
        "username": ctx.message.author.name,
    }
    animeSearch.insert_one(dbStore)
    try:
        await ctx.message.add_reaction('🔍')
        asrc = ani.search('anime', animeQuery)['results'][0]
        mal_id = asrc['mal_id']
        more_info = ani.anime(mal_id)
        trailer_url = more_info['trailer_url']
        if(not trailer_url == None):
            embed = discord.Embed(title=more_info['title'], url=str(more_info['trailer_url']), description="Youtube", color=0x6bffb8)
        else:
            embed = discord.Embed(title=more_info['title'], description="No Trailer available", color=0x6bffb8)
        try:
            embed.set_author(name=more_info['title_japanese'], url=asrc['url'])
        except:
            embed.set_author(name=asrc['title'], url=asrc['url'])
        try:
            embed.set_image(url=asrc['image_url'])
        except:
            pass
        embed.set_thumbnail(url=asrc['image_url'])
        embed.add_field(name="Studio", value=str(
            more_info['studios'][0]['name']), inline=True)
        embed.add_field(name="Started Airing",value=f"{asrc['start_date'][:10]}", inline=True)
        embed.add_field(name="Rating", value=f"{asrc['score']}/10", inline=True)
        embed.add_field(name="Synopsis", value=str(more_info['synopsis'][:512])+'...', inline=False)
        embed.add_field(name="Episodes", value=str(asrc['episodes']), inline=False)
        embed.add_field(name="Views", value=str(asrc['members']), inline=True)
        embed.add_field(name="Rated", value=str(asrc['rated']), inline=True)
        embed.add_field(name="Openings", value=list_to_string(more_info['opening_themes'], 4), inline=False)
        embed.add_field(name="Endings", value=list_to_string(more_info['ending_themes'], 4), inline=False)
        embed.set_footer(text=f"Try typing full name if its incorrect :D", icon_url=self_avatar)
        await ctx.send(embed=embed)
    except:
        try:
            await ctx.message.add_reaction('🔍')
            asrc = ani.search('anime', animeQuery)['results'][1]
            mal_id = asrc['mal_id']
            more_info = ani.anime(mal_id)
            trailer_url = more_info['trailer_url']
            if(not trailer_url == None):
                embed = discord.Embed(title=more_info['title'], url=str(more_info['trailer_url']), description="Youtube", color=0x6bffb8)
            else:
                embed = discord.Embed(title=more_info['title'], description="No Trailer available", color=0x6bffb8)
            try:
                embed.set_author(name=more_info['title_japanese'], url=asrc['url'])
            except:
                embed.set_author(name=asrc['title'], url=asrc['url'])
            embed.set_thumbnail(url=asrc['image_url'])
            embed.add_field(name="Studio", value=str(more_info['studios'][0]['name']), inline=True)
            embed.add_field(name="Started Airing",value=f"{asrc['start_date'][:10]}", inline=True)
            embed.add_field(name="Rating", value=f"{asrc['score']}/10", inline=True)
            embed.add_field(name="Synopsis", value=str(more_info['synopsis'][:512])+'...', inline=False)
            embed.add_field(name="Episodes", value=str(asrc['episodes']), inline=False)
            embed.add_field(name="Views", value=str(asrc['members']), inline=True)
            embed.add_field(name="Rated", value=str(asrc['rated']), inline=True)
            embed.add_field(name="Openings", value=list_to_string(more_info['opening_themes'], 4), inline=False)
            embed.add_field(name="Endings", value=list_to_string(more_info['ending_themes'], 4), inline=False)
            embed.set_footer(text=f"Check the spelling or Try typing full name if its incorrect :D", icon_url=self_avatar)
            await ctx.send(embed=embed)
        except:
            await ctx.message.add_reaction('😭')
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="Anime Not Found", value="That Anime is not found on MyAnimeList", inline=False)
            embed.set_footer(text=self_name, icon_url=self_avatar)
            await ctx.send(embed=embed)


@client.command(aliases=['man', 'm'])
async def manga(ctx, *Query):
    global  ani
    mangaQuery = queryToName(Query)
    dbStore = {
        "charname": mangaQuery,
        "username": ctx.message.author.name,
    }
    mangaSearch.insert_one(dbStore)
    try:
        await ctx.message.add_reaction('🔍')
        asrc = ani.search('manga', mangaQuery)['results'][0]

        embed = discord.Embed(title="Manga Search result",description=asrc['mal_id'], color=0x3dff77)
        embed.set_author(name=asrc['title'], url=asrc['url'])
        embed.set_thumbnail(url=asrc['image_url'])
        embed.add_field(name="Publishing",value=f"{asrc['start_date'][:10]}", inline=False)
        embed.add_field(name="Rating", value=f"{int(asrc['score'])}/10", inline=False)
        embed.add_field(name="Summary", value=asrc['synopsis'], inline=False)
        embed.add_field(name="Volumes", value=asrc['volumes'], inline=True)
        embed.add_field(name="Chapters", value=asrc['chapters'], inline=True)
        embed.add_field(name="Members Watched",value=asrc['members'], inline=True)
        try:
            embed.set_image(url=asrc['image_url'])
        except:
            pass
        embed.set_footer(text=f"Not the right manga .. try searching with its full title", icon_url=client.user.avatar_url)
        await ctx.reply(embed=embed)
    except:
        await ctx.message.add_reaction('😿')
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Manga Not Found", value="That manga was not found on MyAnimeList.. webtoons are not yet supported", inline=False)
        await ctx.reply(embed=embed)

    return


@client.command()
async def hug(ctx, member: discord.Member):
    hgp = member
    await ctx.message.add_reaction('🤗')
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(title=f"{ctx.message.author.mention} hugs themselves",description=f"Don't worry {ctx.message.author.mention}.. {choice(perks['replies']['sadhugs'])}", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['sadhugs']))
    else:
        embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} hugs {hgp.mention}", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['hugs']))
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{self_name}", icon_url=self_avatar)
    await ctx.reply(embed=embed)


@client.command()
async def invite(ctx):
    await ctx.message.add_reaction('♥')
    embed=discord.Embed(title="Click here", url="https://discord.com/api/oauth2/authorize?client_id=709426015759368282&permissions=8&scope=bot", description="Invite link for this bot", color=0xff2429)
    embed.set_thumbnail(url=self_avatar)
    await ctx.reply(embed=embed)

@client.command(aliases=['g'])
async def gpt(ctx, *lquery):
    await ctx.message.add_reaction('💡')
    query = queryToName(lquery)
    reply = g2a.gptquery(query)
    await ctx.reply(reply)
    dbStore = {
                "query": query,
                "username": ctx.message.author.name,
                "reply": reply
            }
    gptDb.insert_one(dbStore)

@client.command()
async def cartoonize(ctx):
    attachment_url = ctx.message.attachments[0].url
    filname = await cartoonize(attachment_url)
    await ctx.send(file=discord.File(f'{filname}.png'))

@client.command(pass_context=True, aliases=['q', 'que'])
async def question(ctx, *lquery):
    await ctx.message.add_reaction('🔎')
    query = queryToName(lquery)
    reply = g2a.questionreply(query)
    await ctx.reply(reply)
    dbStore = {
        "query": query,
        "username": ctx.message.author.name,
        "reply": reply
    }
    gptDb.insert_one(dbStore)

@client.command()
async def kiss(ctx, member: discord.Member):
    hgp = member
    await ctx.message.add_reaction('👄')
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(
            title=" ", description=f"{ctx.message.author.mention} kisses themselves..HOW!!!?", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['erotic_perv']))
    else:
        embed = discord.Embed(
            title="💋", description=f"{ctx.message.author.mention} kisses {hgp.mention}", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['kiss']))
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}",
                     icon_url=client.user.avatar_url)
    await ctx.reply(embed=embed)

@client.command()
async def kill(ctx, member: discord.Member):

    hgp = member
    await ctx.message.add_reaction('🔪')
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} you know there are better ways for than .. than to ask me", colour=discord.Colour(0x00ffb7))
        embed.set_image(url="https://i.pinimg.com/originals/53/4d/f2/534df2eed76c2b48bc9f892086f1e749.jpg")
    else:
        embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} kills {hgp.mention}", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['kill']))
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}",icon_url=client.user.avatar_url)
    await ctx.reply(embed=embed)


@client.command()
async def pat(ctx, member: discord.Member):
    hgp = member
    await ctx.message.add_reaction('👊')
    print(hgp)
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} pats themselves", colour=discord.Colour(0x00ffb7))
        embed.add_field(name="👋", value=f"{ctx.message.author.mention}.. i'll pat you :3")
        embed.set_image(url=choice(perks['links']['pats']))
    else:
        embed = discord.Embed(title=" ", description=f"{ctx.message.author.mention} pats {hgp.mention}", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['pats']))
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}",
                     icon_url=client.user.avatar_url)
    await ctx.reply(embed=embed)


@client.command()
async def bruh(ctx, *qlink):
    link = queryToName(qlink)
    if(ctx.message.guild == None):
        await ctx.reply("This is a dm tho? try it in a server m8")
    else:
        if(link == ""):
            try:
                await ctx.reply(str(bruhs.find_one({"guild": ctx.message.guild.id})['link']))
            except:
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(name="No Bruh found",
                                value=f"Consider adding Bruh using {command_prefix}Bruh <value> ; Value can be Link , Text  ...", inline=False)
                embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
                await ctx.message.channel.send(embed=embed)
        else:
            if(bruhs.find_one({"guild": ctx.message.guild.id}) == None):
                dbStore = {
                    "guild": ctx.message.guild.id,
                    "link": link
                }
                bruhs.insert_one({"guild": ctx.message.guild.id}, dbStore)
            else:
                dbStore = {
                    "guild": ctx.message.guild.id,
                    "link": link
                }
                bruhs.replace_one({"guild": ctx.message.guild.id}, dbStore)
            if(bruhs.find_one({"guild": ctx.message.guild.id}) == None):
                dbStore = {
                    "guild": ctx.message.guild.id,
                    "link": link
                }
                bruhs.insert_one({"guild": ctx.message.guild.id}, dbStore)
            else:
                dbStore = {
                    "guild": ctx.message.guild.id,
                    "link": link
                }
                bruhs.replace_one({"guild": ctx.message.guild.id}, dbStore)
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name="Bruh Updated",
                            value="Bruh has been sucessfully updated", inline=False)
            embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
            await ctx.message.channel.send(embed=embed)

@client.command()
async def stats(ctx):
    embed = discord.Embed(color=0xf3d599)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    try:
        embed.add_field(name="Pacchu's Slave stat counter",value="shows all the statistics of the bot", inline=False)
        embed.add_field(name="Weebo Anime searches",value=str(animeSearch.count_documents({"guild":ctx.message.guild.id})), inline=True)
        embed.add_field(name="Weebo Manga searches",value=str(mangaSearch.count_documents({"guild": ctx.message.guild.id})), inline=True)
        embed.add_field(name="Anime images delivered for simps",value=str(animePics.count_documents({"guild": ctx.message.guild.id})), inline=True)
        embed.set_footer(text=f"MongoDB Connection Active 🟢", icon_url=self_avatar)
        await ctx.send(embed=embed)
    except KeyError:
        embed.add_field(name="Database API cannot be reachable 🔴",
                        value="404?", inline=True)
        embed.set_footer(text=f"Facebook doesnt sponser this btw", icon_url=self_avatar)
        await ctx.send(embed=embed)

@client.command()
async def spotify(ctx, user:discord.Member = None):
    await ctx.message.add_reaction('🎵')
    if user == None:
        user = ctx.author
        pass
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, discord.Spotify):
                embed = discord.Embed(title = f"{user.name}'s Spotify",description = "Listening to {}".format(activity.title),color = 0x1DB954)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(
                            title = f"{user.name}'s Spotify",
                            description = "Not Listening to anything",
                            color = 0x1DB954)
                await ctx.reply(embed=embed)
@client.event
async def on_message(message):
    global client, botcount, currentcount, http, command_prefix
    if(message.author == client.user or message.author.bot):
        return

    for x in message.mentions:
        if(x == client.user):
            await message.channel.send(choice(perks['replies']['pings']))
    #try:
    if("pacchu" in message.content.lower()):
        await message.channel.send('**Hail Pacchu**')
    await client.process_commands(message)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    StartTime = 0
    lastPod = None
    def __init__(self, bot):
        self.bot = bot


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
            embed.add_field(name=f"No Recent Podcast Searches",value=f"search for podcast using {command_prefix}pod",inline=False)
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
            embed.add_field(name=f"{command_prefix}pod", value="This very command you ran",inline=False)
            embed.add_field(name=f"{command_prefix}pod [Name of Podcast]",value="Searches for the Podcast and shows Episodes related to it.", inline=False)
            embed.add_field(name=f"{command_prefix}pod [Name of Podcast] : [Selection Number] or {command_prefix}podp [Selection No]", value="Play the podcast selection , default 0 plays the latest available episode",inline=False)
            embed.add_field(name=f"{command_prefix}stop or {command_prefix}dc",value="Stop and Disconnect\n Sadly Haven't Implemented any Pause for now", inline=False)
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
                    embed.add_field(name="Change Page",value=f"```{command_prefix}pod {podname} - [Page_Number]```")
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
            embed.set_footer(text=client.user.name,icon_url=client.user.avatar_url)
            await ctx.voice_client.disconnect()
            return await ctx.reply(embed=embed)
        else:
            await ctx.message.add_reaction('❗')
            embed = discord.Embed( title=f"you are not in the voice channel", colour=discord.Colour(0xff5065))
            embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            embed.set_footer(text=client.user.name,icon_url=client.user.avatar_url)
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
                embed.set_footer(text=client.user.name,icon_url=client.user.avatar_url)
                return await ctx.send(embed=embed)

        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

client.add_cog(Music(client))
client.run(db['discordToken'].find_one({"botname": "tracebot"})['token'])
