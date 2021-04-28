from __imports__ import *
from gpt2api import *

# File Imports
jsonfile = io.open("perks.json", mode="r", encoding="utf-8")
perks = json.load(jsonfile)

#database stuff
client = MongoClient('mongodb+srv://pacchu:kiminonawa@pslave.da85h.mongodb.net/test')
db = client['PacchuSlave']
## collection variables

serverstat = db['serverstat']
bruhs = db['bruh']
animeSearch = db['animeSearch']
charSearch = db['charSearch']
animePics = db['animePics']
mangaSearch = db['mangaSearch']
gptDb = db['gptQuery']
#PodcastDb = db['PodcastQ']
PodcastSuggest = db['PodSuggest']

# global variables
serverlist = {}  # gonna be removed next
version = "v0.4.4 mongoDB edition"
http = urllib3.PoolManager()
ani = Jikan()
self_name = "Pacchu's Slave"
self_avatar = "https://raw.githubusercontent.com/itspacchu/Pacchu-s-Slave/master/Screenshot%202021-04-09%20225421.png"  # copy pacchu's dp
command_prefix = '_'

# Discord bot
client = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)
guild_ids = [685469328929587268]



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


@slash.slash(name="test",description="This is just a test command, nothing more.")
async def test(ctx):
  await ctx.send(content="Yeeting from documentation is fun amiright")


@slash.slash(name="help",description="Shows all the help commands of this bot :D")
@client.command()
async def help(ctx,kwargs = ''):
    embed = discord.Embed(color=0xae00ff, description=f"Created by Pacchu")
    embed.set_author(name=self_name, icon_url=self_avatar)
    embed.set_thumbnail(url=self_avatar)
    embed.add_field(name="How can I help you",
                    value=f"{self_name} commands", inline=False)
    embed.add_field(name=f"{command_prefix}anime",
                    value="Searches for given anime", inline=True)
    embed.add_field(name=f"{command_prefix}manga",
                    value="Searches for give Manga", inline=True)
    embed.add_field(name=f"{command_prefix}anichar",
                    value="Searches for given Anime Charactor ", inline=True)
    embed.add_field(name=f"{command_prefix}anipics",
                    value="Searches for Images of given Anime Charactor", inline=True)
    embed.add_field(name=f"{command_prefix}avatar @mention",
                    value="Steals the person's DP :d", inline=False)
    embed.add_field(name=f"{command_prefix}stats",
                    value="disabled **bugs**", inline=False)
    embed.add_field(name=f"{command_prefix}help",
                    value="isnt it obvious :o", inline=False)
    embed.add_field(name=f"{command_prefix}perk",
                    value="Extra stuff run the command for more commands", inline=False)
    embed.set_footer(text=f"{self_name} {version}", icon_url=self_avatar)
    try:
        await ctx.reply(embed=embed)
    except AttributeError:
        await ctx.send(embed=embed)


@slash.slash(name="perks",description="Shows the perks")
@client.command()
async def perk(ctx):
    embed = discord.Embed(title=client.user.name.title(),
                          description=f"{self_name} Perks", color=0xff9500)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="Noice m8", value=f"nice nice nice :D", inline=False)
    embed.add_field(name="Ping me?",
                    value=f"I Know when you ping me", inline=False)
    embed.add_field(name=f"{command_prefix}kill @mention",
                    value=f"Kills the user ... well not really", inline=False)
    embed.add_field(name=f"{command_prefix}kiss @mention",
                    value=f"Kisses the user? not a good proposal material.", inline=False)
    embed.add_field(name=f"{command_prefix}hug @mention",
                    value=f"Hugs the user?", inline=False)
    embed.add_field(name=f"{command_prefix}avatar @mention",
                    value=f"Something of use atleast", inline=False)
    embed.add_field(name=f"{command_prefix}bruh",
                    value=f"{command_prefix} bruh [image/text]", inline=False)
    embed.add_field(name=f"{command_prefix}irumachi",
                    value="Sends an Adorable photo of irumakun from Marimashita irumakun", inline=False)
    embed.add_field(name=f"{command_prefix}gpt",
                    value="Sends a query response from openai gpt2 model", inline=False)
    embed.set_footer(text=f" {client.user.name} {version}",
                     icon_url=client.user.avatar_url)  
    try:
        await ctx.reply(embed=embed)
    except AttributeError:
        await ctx.send(embed=embed)

@slash.slash(name="avatar",description="Shows the avatar of the person mentioned")
@client.command()
async def avatar(ctx, member: discord.Member):
    global serverlist
    hgp = member
    await ctx.message.add_reaction('🙄')
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(
            title="OwO", description=f"{ctx.message.author.mention} steals ...wait thats your OWN", colour=discord.Colour(0xa06a6a))
        embed.set_image(url=ctx.message.author.avatar_url)
    else:
        embed = discord.Embed(
            title="Beep Boop", description=f"{ctx.message.author.mention} steals {hgp.mention}'s profile pic 👀'", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=hgp.avatar_url)

    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}",
                     icon_url=client.user.avatar_url)
    try:
        await ctx.reply(embed=embed)
    except AttributeError:
        await ctx.send(embed=embed)


@slash.slash(name="animechar",description="Searches for the anime character from Myanimelist")
@client.command()
async def anichar(ctx, *Query):
    global serverlist, ani
    animeQuery = queryToName(Query)
    try:
        await ctx.message.add_reaction('🔍')
        asrc = ani.character(ani.search('character', str(animeQuery))[
                             'results'][0]['mal_id'])
        if(len(asrc['about']) < 511):
            embed = discord.Embed(title=f"**{asrc['name']}**", colour=discord.Colour(
                0xa779ff), url=asrc['url'], description=asrc['about'].strip().replace(r'\n', '')+'...')
        else:
            embed = discord.Embed(title=f"**{asrc['name']}**", colour=discord.Colour(
                0xa779ff), url=asrc['url'], description=asrc['about'][512].strip().replace(r'\n', '')+'...')
        embed.set_image(url=asrc['image_url'])
        embed.set_footer(
            text=f"Not the correct Character ... Try spelling their full name", icon_url=client.user.avatar_url)
        embed.add_field(
            name="Waifu Vote", value=f"{asrc['member_favorites']} have liked them", inline=False)
        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.send(embed=embed)
        try:
            #datastore
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
        embed.add_field(name="Character Not Found",
                        value="That Character is not found ", inline=False)
        embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.send(embed=embed)


@client.command()
async def anipics(ctx, *Query):
    global serverlist, ani, http
    charQuery = queryToName(Query)
    try:
        await ctx.message.add_reaction('🔍')
        charid = ani.search('character', charQuery)['results'][0]
        url = f"https://api.jikan.moe/v3/character/{charid['mal_id']}/pictures"
        picdat = json.loads(http.request('GET', url).data.decode())['pictures']
        embed = discord.Embed(
            title=f"**{charid['name']}**", colour=discord.Colour(0xa779ff), url=charid['url'])
        embed.set_image(url=choice(picdat)['small'])
        embed.set_footer(
            text=f"Not the correct charector... Try spelling their full name", icon_url=client.user.avatar_url)
        await ctx.reply(embed=embed)
        try:
            #datastore
            dbStore = {
                "charname":charQuery,
                "username": ctx.message.author.name,
                "guild": ctx.message.guild.id
            }
        except AttributeError:
            dbStore = {
                "charname": charQuery,
                "username": ctx.message.author.name,
                "guild": "DirectMessage"
            }
        animePics.insert_one(dbStore)
    except:
        await ctx.message.add_reaction('😞')
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Images Not Found",
                        value=" Coudn't find any images on given Query ", inline=False)
        embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
        await ctx.reply(embed=embed)


@client.command()
async def anime(ctx, *Query):
    global serverlist, ani
    animeQuery = queryToName(Query)
    try:
    #datastore
        dbStore = {
            "charname": animeQuery,
            "username": ctx.message.author.name,
            "guild":ctx.message.guild.id
        }
    except AttributeError:
        dbStore = {
            "charname": animeQuery,
            "username": ctx.message.author.name,
            "guild": "DirectMessage"
        }
    animeSearch.insert_one(dbStore)
    
    try:
        await ctx.message.add_reaction('🔍')
        asrc = ani.search('anime', animeQuery)['results'][0]
        mal_id = asrc['mal_id']
        more_info = ani.anime(mal_id)
        trailer_url = more_info['trailer_url']
        if(not trailer_url == None):
            embed = discord.Embed(title=more_info['title'], url=str(
                more_info['trailer_url']), description="Youtube", color=0x6bffb8)
        else:
            embed = discord.Embed(
                title=more_info['title'], description="No Trailer available", color=0x6bffb8)
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
        embed.add_field(name="Started Airing",
                        value=f"{asrc['start_date'][:10]}", inline=True)
        embed.add_field(
            name="Rating", value=f"{asrc['score']}/10", inline=True)
        embed.add_field(name="Synopsis", value=str(
            more_info['synopsis'][:512])+'...', inline=False)
        embed.add_field(name="Episodes", value=str(
            asrc['episodes']), inline=False)
        embed.add_field(name="Views", value=str(asrc['members']), inline=True)
        embed.add_field(name="Rated", value=str(asrc['rated']), inline=True)
        embed.add_field(name="Openings", value=list_to_string(
            more_info['opening_themes'], 4), inline=False)
        embed.add_field(name="Endings", value=list_to_string(
            more_info['ending_themes'], 4), inline=False)
        embed.set_footer(
            text=f"Check the spelling or Try typing full name if its incorrect :D", icon_url=self_avatar)
        await ctx.send(embed=embed)
    except:
        try:
            await ctx.message.add_reaction('🔍')
            asrc = ani.search('anime', animeQuery)['results'][1]
            mal_id = asrc['mal_id']
            more_info = ani.anime(mal_id)
            trailer_url = more_info['trailer_url']
            if(not trailer_url == None):
                embed = discord.Embed(title=more_info['title'], url=str(
                    more_info['trailer_url']), description="Youtube", color=0x6bffb8)
            else:
                embed = discord.Embed(
                    title=more_info['title'], description="No Trailer available", color=0x6bffb8)
            try:
                embed.set_author(
                    name=more_info['title_japanese'], url=asrc['url'])
            except:
                embed.set_author(name=asrc['title'], url=asrc['url'])

            try:
                embed.set_image(url=asrc['image_url'])
            except:
                pass
            embed.set_thumbnail(url=asrc['image_url'])
            embed.add_field(name="Studio", value=str(
                more_info['studios'][0]['name']), inline=True)
            embed.add_field(name="Started Airing",
                            value=f"{asrc['start_date'][:10]}", inline=True)
            embed.add_field(
                name="Rating", value=f"{asrc['score']}/10", inline=True)
            embed.add_field(name="Synopsis", value=str(
                more_info['synopsis'][:512])+'...', inline=False)
            embed.add_field(name="Episodes", value=str(
                asrc['episodes']), inline=False)
            embed.add_field(name="Views", value=str(
                asrc['members']), inline=True)
            embed.add_field(name="Rated", value=str(
                asrc['rated']), inline=True)
            embed.add_field(name="Openings", value=list_to_string(
                more_info['opening_themes'], 4), inline=False)
            embed.add_field(name="Endings", value=list_to_string(
                more_info['ending_themes'], 4), inline=False)
            embed.set_footer(
                text=f"Check the spelling or Try typing full name if its incorrect :D", icon_url=self_avatar)
            await ctx.send(embed=embed)
        except:
            await ctx.message.add_reaction('😭')
            embed = discord.Embed(color=0xff0000)
            embed.add_field(
                name="Anime Not Found", value="That Anime is not found on MyAnimeList", inline=False)
            embed.set_footer(text=self_name, icon_url=self_avatar)
            await ctx.send(embed=embed)


@client.command()
async def manga(ctx, *Query):
    global serverlist, ani
    mangaQuery = queryToName(Query)
    try:
        #datastore
        dbStore = {
            "charname": mangaQuery,
            "username": ctx.message.author.name,
            "guild":ctx.message.guild.id
        }
    except AttributeError:
        dbStore = {
            "charname": charQuery,
            "username": ctx.message.author.name,
            "guild": "DirectMessage"
        }
    mangaSearch.insert_one(dbStore)
    
    try:
        await ctx.message.add_reaction('🔍')
        asrc = ani.search('manga', mangaQuery)['results'][0]

        embed = discord.Embed(title="Manga Search result",
                              description=asrc['mal_id'], color=0x3dff77)
        embed.set_author(name=asrc['title'], url=asrc['url'])
        embed.set_thumbnail(url=asrc['image_url'])
        embed.add_field(name="Publishing",
                        value=f"{asrc['start_date'][:10]}", inline=False)
        embed.add_field(
            name="Rating", value=f"{int(asrc['score'])}/10", inline=False)
        embed.add_field(name="Summary", value=asrc['synopsis'], inline=False)
        embed.add_field(name="Volumes", value=asrc['volumes'], inline=True)
        embed.add_field(name="Chapters", value=asrc['chapters'], inline=True)
        embed.add_field(name="Members Watched",
                        value=asrc['members'], inline=True)
        try:
            embed.set_image(url=asrc['image_url'])
        except:
            pass
        embed.set_footer(
            text=f"Not the right manga .. try searching with its full title", icon_url=client.user.avatar_url)
        await ctx.reply(embed=embed)

    except:
        await ctx.message.add_reaction('😿')
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Manga Not Found",
                        value="That manga was not found on MyAnimeList.. webtoons are not yet supported", inline=False)
        await ctx.reply(embed=embed)

    return


@client.command()
async def hug(ctx, member: discord.Member):
    global serverlist
    hgp = member
    await ctx.message.add_reaction('🤗')
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(title=f"{ctx.message.author.mention} hugs themselves",
                              description=f"Don't worry {ctx.message.author.mention}.. {choice(perks['replies']['sadhugs'])}", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['sadhugs']))
    else:
        embed = discord.Embed(
            title=" ", description=f"{ctx.message.author.mention} hugs {hgp.mention}", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['hugs']))

    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{self_name}", icon_url=self_avatar)
    await ctx.reply(embed=embed)
    

@client.command()
async def gpt(ctx, *lquery):
    await ctx.message.add_reaction('💡')
    query = queryToName(lquery)
    reply = gptquery(query)
    await ctx.reply(reply)
    dbStore = {
                "query": query,
                "username": ctx.message.author.name,
                "reply": reply
            }
    gptDb.insert_one(dbStore)

@client.command()
async def podsuggest(ctx, *lquery):
    await ctx.message.add_reaction('🙏')
    query = queryToName(lquery)
    await ctx.reply(f"Added ```{query}```Podcast would be added as soon as its added in Database")
    dbStore = {
                "suggestion": query,
                "username": ctx.message.author.name,
            }
    PodcastSuggest.insert_one(dbStore)


@client.command(pass_context=True, aliases=['q', 'que'])
async def question(ctx, *lquery):
    await ctx.message.add_reaction('🔎')
    query = queryToName(lquery)
    reply = questionreply(query)
    await ctx.reply(reply)
    dbStore = {
        "query": query,
        "username": ctx.message.author.name,
        "reply": reply
    }
    gptDb.insert_one(dbStore)


@client.command()
async def kiss(ctx, member: discord.Member):
    global serverlist
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
    global serverlist
    hgp = member
    await ctx.message.add_reaction('🔪')
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(
            title=" ", description=f"{ctx.message.author.mention} you know there are better ways for than .. than to ask me", colour=discord.Colour(0x00ffb7))
        embed.set_image(
            url="https://i.pinimg.com/originals/53/4d/f2/534df2eed76c2b48bc9f892086f1e749.jpg")
    else:
        embed = discord.Embed(
            title=" ", description=f"{ctx.message.author.mention} kills {hgp.mention}", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['kill']))
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}",
                     icon_url=client.user.avatar_url)
    await ctx.reply(embed=embed)


@client.command()
async def pat(ctx, member: discord.Member):
    global serverlist
    hgp = member
    await ctx.message.add_reaction('👊')
    print(hgp)
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(
            title=" ", description=f"{ctx.message.author.mention} pats themselves", colour=discord.Colour(0x00ffb7))
        embed.add_field(
            name="👋", value=f"{ctx.message.author.mention}.. i'll pat you :3")
        embed.set_image(url=choice(perks['links']['pats']))
    else:
        embed = discord.Embed(
            title=" ", description=f"{ctx.message.author.mention} pats {hgp.mention}", colour=discord.Colour(0x00ffb7))
        embed.set_image(url=choice(perks['links']['pats']))
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}",
                     icon_url=client.user.avatar_url)
    await ctx.reply(embed=embed)


@client.command()
async def bruh(ctx, *qlink):
    link = queryToName(qlink)
    global serverlist
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
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name="Bruh Updated",
                            value="Bruh has been sucessfully updated", inline=False)
            embed.set_footer(text=f" {self_name} {version}", icon_url=self_avatar)
            await ctx.message.channel.send(embed=embed)


@client.command()
async def irumachi(ctx):
    await ctx.reply(choice(perks["links"]["iruma"]))


@client.command()
async def stats(ctx):
    global serverlist
    embed = discord.Embed(color=0xf3d599)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    try:
        embed.add_field(name="Pacchu's Slave stat counter",
                        value="shows all the statistics of the bot", inline=False)
        embed.add_field(name="Weebo Anime searches",
                        value=str(animeSearch.count_documents({"guild":ctx.message.guild.id})), inline=True)
        embed.add_field(name="Weebo Manga searches",
                        value=str(mangaSearch.count_documents({"guild": ctx.message.guild.id})), inline=True)
        embed.add_field(name="Anime images delivered for simps",
                        value=str(animePics.count_documents({"guild": ctx.message.guild.id})), inline=True)
        embed.set_footer(
            text=f"MongoDB Connection Active 🟢", icon_url=self_avatar)
        await ctx.send(embed=embed)
    except KeyError:
        embed.add_field(name="Database API cannot be reachable 🔴",
                        value="404?", inline=True)
        embed.set_footer(text=f"Facebook doesnt sponser this btw", icon_url=self_avatar)
        await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=['Pacchu', '94cchu'])
async def pacchu(ctx):
    await ctx.reply('Hail pacchu')



@client.command()
async def spotify(ctx, user:discord.Member = None):
    await ctx.message.add_reaction('🎵')
    if user == None:
        user = ctx.author
        pass
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed = discord.Embed(
                    title = f"{user.name}'s Spotify",
                    description = "Listening to {}".format(activity.title),
                    color = 0x1DB954)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                embed.set_footer(text="Listening Since {}".format(activity.created_at.strftime("%H:%M")))
                await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
                    title = f"{user.name}'s Spotify",
                    description = "Not Listening to anything",
                    color = 0x1DB954)
        await ctx.reply(embed=embed)
        


@client.event
async def on_message(message):
    global darkemoji, client, botcount, serverlist, currentcount, http, command_prefix
    if message.author == client.user:
        return

    for x in message.mentions:
        if(x == client.user):
            await message.channel.send(choice(perks['replies']['pings']))
    #try:
    await client.process_commands(message)
    #except:
    #    print("dis has error")


###################################################################################################################################### Yeeting someone's code
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

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
            embed = discord.Embed(
                title=f"Searching : {str(url)}", colour=discord.Colour(0xff5065))
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=None)

        
        embed.set_author(name=ctx.message.author.name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=self_name, icon_url=self_avatar)
        await ctx.reply(embed=embed)
        
    @commands.command(pass_context=True, aliases=['pl'])
    async def lofi(self, ctx, *, url="https://youtu.be/5qap5aO4i9A"):
        await ctx.message.add_reaction('🎧')
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=None)
            embed = discord.Embed(title="Playing from Youtube", colour=discord.Colour(
                0xff5065), url=url, description=player.title)
            embed.set_image(
                url="https://i.ytimg.com/vi/5qap5aO4i9A/maxresdefault.jpg")
        embed.set_author(name=ctx.message.author.name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=self_name, icon_url=self_avatar)
        await ctx.reply(embed=embed)
    
    @commands.command(aliases=['podplay', 'podcast'])
    async def pod(self,ctx , * , strparse = " "):
        await ctx.message.add_reaction('🔎')
        if(':' in strparse):
            podname,num = strparse.replace(' ','').split(':')
            podepi = int(num)
        elif(not strparse == ' '):
            podname = strparse.replace(' ','')
            podepi = None
        else:
            podname = ' '
            podepi = None
        
        all_pods = [ph.podcasts[x]['name'] for x in ph.podcasts]
        if(podname == " "):
            await ctx.send('Enter the podcast name you want to listen to')
            embed = discord.Embed(colour=discord.Colour(0xbd10e0), description="All the supported podcasts for now [ usage pod name:episode ]")

            embed.set_thumbnail(url=self_avatar)
            embed.set_author(name=self_name, url=self_avatar,
                             icon_url=self_avatar)

            embed.set_footer(text="Page 1/1", icon_url=self_avatar)
            for singlepod in ph.podcasts:
                embed.add_field(name=ph.podcasts[singlepod]['name'],
                                value=str(ph.podcasts[singlepod]['rss']) )
        
        if(podepi == None and not podname == " "):
            await ctx.send(f'Searching for episodes in {podname}')
            embed = discord.Embed(colour=discord.Colour(
                0xbd10e0), description=" ")

            embed.set_thumbnail(url=self_avatar)
            embed.set_author(name=self_name, url=self_avatar,
                             icon_url=self_avatar)

            embed.set_footer(text=f"Page 1/NaN", icon_url=self_avatar)
            k = ph.podcasts[all_pods.index(podname.lower().replace(' ', ''))]
            currentpod = ph.Podcast(k['name'], k['rss'])
            ind = 0
            for episode_ in currentpod.ListEpisodes():
                embed.add_field(name=episode_,value=f"Select {ind} from "+podname)
                ind += 1
                if(ind > 10):
                    break
        
        if(not podepi == None and not podname == " "):
            k = ph.podcasts[all_pods.index(podname.lower().replace(' ', ''))]
            currentpod = ph.Podcast(k['name'], k['rss'])
            await self.playPodcast(ctx,podepi=podepi,currentpod=currentpod,k=k)  
            embed = discord.Embed(title=currentpod.GetEpisodeDetails(podepi)['title'], 
                                  colour=discord.Colour(0xb8e986), url=currentpod.GetEpisodeDetails(podepi)['link'],
                                  description=currentpod.GetEpisodeDetails(podepi)['summary'])
            embed.set_thumbnail(url=currentpod.PodcastImage(podepi))
            embed.set_author(name=self_name, 
                             icon_url=self_avatar)
            embed.set_footer(text="Alpha",
                 icon_url=self_avatar)
        await ctx.send(embed=embed)
    
    async def playPodcast(self, context, podepi, currentpod, k):
        guild = context.guild
        voice_client: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=guild)
        _source_ = currentpod.GetEpisodeMp3(podepi)
        audio_source = discord.FFmpegPCMAudio(_source_)
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)

    @commands.command()
    async def stop(self, ctx ):
        await ctx.message.add_reaction('👍')
        """Stops and disconnects the bot from voice"""
        embed = discord.Embed(
            title=f"Exiting", colour=discord.Colour(0xff5065))
        embed.set_author(name=ctx.message.author.name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=client.user.name,
                         icon_url=client.user.avatar_url)
        await ctx.voice_client.disconnect()
        return await ctx.reply(embed=embed)

    @lofi.before_invoke
    @play.before_invoke
    @pod.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice.channel:
                await ctx.author.voice.channel.connect()
            else:
                embed = discord.Embed(
                    title=f"{ctx.message.author.mention} is not connected to any Voice channel", colour=discord.Colour(0xff5065))
                embed.set_author(name=ctx.message.author.name,
                                 icon_url=ctx.message.author.avatar_url)
                embed.set_footer(text=client.user.name,
                                 icon_url=client.user.avatar_url)
                return await ctx.send(embed=embed)

        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            
    
        



            
client.add_cog(Music(client))


##################################################################################################################################### End

client.run(db['discordToken'].find_one({"botname": "pacchuslave"})['token'])
