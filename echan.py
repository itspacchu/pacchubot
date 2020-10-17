# IMPORTS

#from time import *
from time import *
from random import *
import time,subprocess,discord,os,json,io
from jikanpy import Jikan
import numpy as np
import urllib3
from discord.ext import commands
from pacchufunctions import __count_statistics__,__initiate_default_stats__,mentionToId,queryToName,list_to_string
from vijaysfunctions import joyreactor , src3 , img2wall , imgbin
# File Imports

jsonfile = io.open("perks.json",mode="r",encoding="utf-8")
perks = json.load(jsonfile)

# global variables

serverlist = {}
version = "v0.4.1 alpha"
http = urllib3.PoolManager()
ani = Jikan()
pacchuid = 170783707647442947
tempid = 569911088141959189


darkemoji = None
emojiname='darkalpha' #defaulted emojiname
anime_reply = False
botcount = 0
currentcount = 0
ecchi_vote = False
command_prefix='_'
# Discord bot


client = commands.Bot(command_prefix='_')
client.remove_command('help')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    statustxt = "Running with 1% confidence"
    activity = discord.Game(name=statustxt)
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.command()
async def help(ctx):
    global pacchuid , tempid

    embed=discord.Embed(color=0xae00ff,description=f"Created by Pacchu and TemperatureWash")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="How can I help you", value=f"{client.user.name} commands", inline=False)
    embed.add_field(name="anime", value="Searches for given anime", inline=True)
    embed.add_field(name="manga", value="Searches for give Manga", inline=True)
    embed.add_field(name="anichar", value="Searches for given Anime Charactor [BETA] ", inline=True)
    embed.add_field(name="anipics", value="Searches for Images of given Anime Charactor [ALPHA] ", inline=True)
    embed.add_field(name="avatar <person>", value="Steals the person's DP :d", inline=False)
    #embed.add_field(name="status newstatus", value="changes status of the bot", inline=False)
    embed.add_field(name="stats", value="Check the stats **PER SERVER STATS**", inline=False)
    embed.add_field(name="bruh", value="bruh", inline=False)
    if (ctx.message.channel.nsfw==True):
        embed.add_field(name="NSFW COMMANDS", value="18+", inline=False)
        embed.add_field(name="recchi", value="gets latest r/ecchi post from reddit [ COMMING SOON ]", inline=False)
        embed.add_field(name="ecchi", value="sends a random nsfw image", inline=False)
        embed.add_field(name="hentai", value="Suggests a random hentai from database [ COMMING SOON ]", inline=False)
        
    embed.add_field(name="irumachi", value="Sends an Adorable photo of irumakun from Marimashita irumakun", inline=False)
    embed.add_field(name="perks", value="Lists the perks of this bot", inline=False)
    embed.add_field(name="help", value="isnt it obvious :o", inline=False)
    embed.set_footer(text=f"{client.user.name} {version}", icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def hug(ctx,username):
    global serverlist
    hgp = client.get_user(mentionToId(username))
    await ctx.message.add_reaction('🤗')
    if(ctx.message.author == hgp  or hgp == None):
        embed = discord.Embed(title=f"{ctx.message.author.mention} hugs themselves",description=f"Don't worry {ctx.message.author.mention}.. {choice(perks['replies']['sadhugs'])}", colour=discord.Colour(0xcd94ff))
        embed.set_image(url=choice(perks['links']['sadhugs']))
    else:
        embed = discord.Embed(title=" ",description=f"{ctx.message.author.mention} hugs {hgp.mention}", colour=discord.Colour(0xcd94ff))
        embed.set_image(url=choice(perks['links']['hugs']))

    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)
    __count_statistics__(serverlist,ctx.guild.id,'hugs')
    
@client.command()
async def avatar(ctx,username):
    global serverlist
    print('avatar fetching..')
    hgp = client.get_user(mentionToId(username))
    await ctx.message.add_reaction('👌')
    if(ctx.message.author == hgp  or hgp == None):
        embed = discord.Embed(title="OwO",description=f"{ctx.message.author.mention} steals ...wait thats your OWN", colour=discord.Colour(0xa06a6a))
        embed.set_image(url=ctx.message.author.avatar_url)
    else:
        embed = discord.Embed(title=" Beeo Boop ",description=f"{ctx.message.author.mention} steals {hgp.mention}'s profile pic 👀'", colour=discord.Colour(0xcd94ff))
        embed.set_image(url=hgp.avatar_url)
        
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def kiss(ctx,username):
    global serverlist
    hgp = client.get_user(mentionToId(username))
    await ctx.message.add_reaction('👄')
    if(ctx.message.author == hgp  or hgp == None):
        embed = discord.Embed(title=" ",description=f"{ctx.message.author.mention} kisses themselves..HOW!!!?", colour=discord.Colour(0xcd94ff))
        embed.set_image(url=choice(perks['links']['erotic_perv']))
    else:
        embed = discord.Embed(title="💋",description=f"{ctx.message.author.mention} kisses {hgp.mention}", colour=discord.Colour(0xcd94ff))
        embed.set_image(url=choice(perks['links']['kiss']))
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)
    __count_statistics__(serverlist,ctx.guild.id,'kiss')

@client.command()
async def kill(ctx,username):
    global serverlist
    hgp = client.get_user(mentionToId(username))
    await ctx.message.add_reaction('🔪')
    if(ctx.message.author == hgp  or hgp == None):
        embed = discord.Embed(title=" ",description=f"{ctx.message.author.mention} you know there are better ways for than .. than to ask me", colour=discord.Colour(0xcd94ff))
        embed.set_image(url="https://i.pinimg.com/originals/53/4d/f2/534df2eed76c2b48bc9f892086f1e749.jpg")
    else:
        embed = discord.Embed(title=" ",description=f"{ctx.message.author.mention} kills {hgp.mention}", colour=discord.Colour(0xcd94ff))
        embed.set_image(url=choice(perks['links']['kill']))
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)
    __count_statistics__(serverlist,ctx.guild.id,'kills')

@client.command()
async def pat(ctx,username):
    global serverlist
    hgp = client.get_user(mentionToId(username))
    await ctx.message.add_reaction('👊')
    if(ctx.message.author == hgp or hgp == None):
        embed = discord.Embed(title=" ",description=f"{ctx.message.author.mention} pats themselves", colour=discord.Colour(0xcd94ff))
        embed.add_field(name="👋", value=f"{ctx.message.author.mention}.. i'll pat you :3")
        embed.set_image(url=choice(perks['links']['pats']))
    else:
        embed = discord.Embed(title=" ",description=f"{ctx.message.author.mention} pats {hgp.mention}", colour=discord.Colour(0xcd94ff))
        embed.set_image(url=choice(perks['links']['pats']))
    embed.set_author(name=hgp.name, icon_url=hgp.avatar_url)
    embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)
    __count_statistics__(serverlist,ctx.guild.id,'pats')

@client.command()
async def perk(ctx):
    embed=discord.Embed(title=client.user.name.title(), description="Ecchi perks ", color=0xff9500)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="Nice Lenny", value=f"searches for nice or noice in messages", inline=False)
    embed.add_field(name="Ping Awareness", value=f"I Know when you ping me", inline=False)
    embed.set_footer(text=f" {client.user.name} {version}", icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def bruh(ctx,link=None):
    global serverlist
    __count_statistics__(serverlist,ctx.guild.id,'bruhs')

    if(link == None):
        try:
            await ctx.send(serverlist[str(ctx.guild.id)]['bruh'])
        except KeyError:
            __initiate_default_stats__(serverlist,str(ctx.guild.id))
            await ctx.send(serverlist[str(ctx.guild.id)]['bruh'])
    else:
        serverlist[str(ctx.guild.id)] = {'bruh':link}
        embed=discord.Embed(color=0x00ff00)
        embed.add_field(name="Bruh image Updated", value="Bruh image has been sucessfully updated", inline=False)
        embed.set_footer(text=f" {client.user.name} v0.4 alpha", icon_url=client.user.avatar_url)
        await ctx.message.channel.send(embed=embed)
    
@client.command()
async def anichar(ctx,*Query):
    global serverlist,ani
    animeQuery = queryToName(Query)
    try:
        await ctx.message.add_reaction('😉')
        asrc = ani.character(ani.search('character',str(animeQuery))['results'][0]['mal_id'])
        if(len(asrc['about']) < 511):
            embed = discord.Embed(title=f"**{asrc['name']}**", colour=discord.Colour(0xa779ff), url=asrc['url'], description=asrc['about'].strip().replace(r'\n','')+'...')
        else:
            embed = discord.Embed(title=f"**{asrc['name']}**", colour=discord.Colour(0xa779ff), url=asrc['url'], description=asrc['about'][512].strip().replace(r'\n','')+'...')
        embed.set_image(url=asrc['image_url'])
        embed.set_footer(text=f"Not the correct Character ... Try spelling their full name", icon_url=client.user.avatar_url)
        embed.add_field(name="Waifu/Husbando-Meter", value=f"{asrc['member_favorites']} have liked them", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.message.add_reaction('😞')
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="Character Not Found", value="That Character is not found ", inline=False)
        embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    __count_statistics__(serverlist,ctx.guild.id,'anichars')

@client.command()
async def anipics(ctx,*Query):
    global serverlist,ani,http
    charQuery = queryToName(Query)
    try:
        await ctx.message.add_reaction('😉')
        charid = ani.search('character',charQuery)['results'][0]
        url = f"https://api.jikan.moe/v3/character/{charid['mal_id']}/pictures"
        picdat = json.loads(http.request('GET',url).data.decode())['pictures']
        embed = discord.Embed(title=f"**{charid['name']}**", colour=discord.Colour(0xa779ff), url=charid['url'])
        embed.set_image(url=choice(picdat)['small'])
        embed.set_footer(text=f"Not the correct charector... Try spelling their full name", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    except:
        await ctx.message.add_reaction('😞')
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="Images Not Found", value=" Coudn't find any images on given Query ", inline=False)
        embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    __count_statistics__(serverlist,ctx.guild.id,'anipics')

@client.command()
async def anime(ctx,*Query):
    global serverlist,ani
    animeQuery = queryToName(Query)
    try:
        await ctx.message.add_reaction('😉')
        asrc = ani.search('anime',animeQuery)['results'][0]
        mal_id = asrc['mal_id']
        more_info = ani.anime(mal_id)

        embed=discord.Embed(title="Trailer", url=more_info['trailer_url'], description="Trailer", color=0x6bffb8)
        try:
            embed.set_author(name=more_info['title_japanese'], url=asrc['url'])
        except:
            embed.set_author(name=asrc['title'], url=asrc['url'])
        embed.set_thumbnail(url=asrc['image_url'])
        embed.add_field(name="Studio", value=more_info['studios'][0]['name'], inline=True)
        embed.add_field(name="Started Airing", value=f"{asrc['start_date'][:10]}", inline=True)
        embed.add_field(name="Rating", value=f"{int(asrc['score'])}/10", inline=True)
        embed.add_field(name="synopsis", value=more_info['synopsis'][:512]+'...', inline=False)
        embed.add_field(name="episodes", value=asrc['episodes'], inline=False)
        embed.add_field(name="views", value=asrc['members'], inline=True)
        embed.add_field(name="Rated", value=asrc['rated'], inline=True) 
        embed.add_field(name="Openings", value=list_to_string(more_info['opening_themes'],4), inline=False)
        embed.add_field(name="Endings", value=list_to_string(more_info['ending_themes'],4), inline=False)

        embed.set_footer(text=f"Not the correct Anime ... use the full name including OVA or TV series", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)   
    except:
        await ctx.message.add_reaction('😭')
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="Anime Not Found", value="That Anime is not found on MyAnimeList", inline=False)
        embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
        __count_statistics__(serverlist,ctx.guild.id,'anime')
    return

@client.command()
async def manga(ctx,*Query):
    global serverlist,ani
    mangaQuery = queryToName(Query)
    try:
        await ctx.message.add_reaction('😉')
        start = time.time()
        asrc = ani.search('manga',mangaQuery)['results'][0]
        end = time.time()
        embed=discord.Embed(title="Manga Search result", description=asrc['mal_id'], color=0x3dff77)
        embed.set_author(name=asrc['title'], url=asrc['url'])
        embed.set_thumbnail(url=asrc['image_url'])
        embed.add_field(name="Started Publishing", value=f"{asrc['start_date'][:10]}", inline=False)
        embed.add_field(name="Rating", value=f"{int(asrc['score'])}/10", inline=False)
        embed.add_field(name="synopsis", value=asrc['synopsis'], inline=False)
        embed.add_field(name="Volumes", value=asrc['volumes'], inline=True)
        embed.add_field(name="chapters", value=asrc['chapters'], inline=True)
        embed.add_field(name="views", value=asrc['members'], inline=True)
        embed.set_footer(text=f"Not the right manga .. try searching with its full title", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
        
    except:
        await ctx.message.add_reaction('😿')
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="Manga Not Found", value="That manga was not found on MyAnimeList.. webtoons are not yet supported", inline=False)
        await ctx.send(embed=embed)
    __count_statistics__(serverlist,ctx.guild.id,'manga')
    return


@client.command()
async def irumachi(ctx):
    await ctx.send(choice(perks["links"]["iruma"]))

@client.command()
async def stats(ctx):
    global serverlist
    embed = discord.Embed(color=0xf3d599)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    try:
        embed.add_field(name="Echan stat counter", value="shows all the statistics of the bot **Server Independant**", inline=False)
        embed.add_field(name="Hugs delivered", value=serverlist[ctx.guild.id]['stats']['hugs'], inline=True)
        embed.add_field(name="Kisses", value=serverlist[ctx.guild.id]['stats']['kiss'], inline=True)
        embed.add_field(name="Pats delivered", value=serverlist[ctx.guild.id]['stats']['pats'], inline=True)
        embed.add_field(name="Kills executed", value=serverlist[ctx.guild.id]['stats']['kills'], inline=True)
        embed.add_field(name="Lennies delivered", value=serverlist[ctx.guild.id]['stats']['nice'], inline=True)
        embed.add_field(name="bruhs delivered", value=serverlist[ctx.guild.id]['stats']['bruhs'], inline=True)
        embed.add_field(name="Weebo Anime searches", value=serverlist[ctx.guild.id]['stats']['anime'], inline=True)
        embed.add_field(name="Weebo Manga searches", value=serverlist[ctx.guild.id]['stats']['manga'], inline=True)
        embed.add_field(name="Anime images delivered for simps", value=serverlist[ctx.guild.id]['stats']['anipics'], inline=True)
        embed.add_field(name="Ecchi summons", value=serverlist[ctx.guild.id]['stats']['ecchi_command'], inline=True)
        embed.set_footer(text=f"data is volatile", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    except KeyError:
        __initiate_default_stats__(serverlist,ctx.guild.id)
        embed.add_field(name="No Data", value="The bot was not run at all T_T pls use me", inline=True)
        embed.set_footer(text=f"data is volatile", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)


@client.command()
async def pacchu(ctx):
    ctx.send('Hail pacchu')


@client.event
async def on_message(message):
    global darkemoji,client,ecchi_vote,botcount,serverlist,currentcount,asrc,http,command_prefix
    if message.author == client.user:
        if(ecchi_vote):
            await message.add_reaction('⬆')
            await message.add_reaction('⬇')
            ecchi_vote = False

    
    for x in message.mentions:
        if(x==client.user):
            await message.channel.send(choice(perks['replies']['pings']) + message.author.mention)

    await client.process_commands(message)

    if(message.content.startswith(command_prefix[0]+'ecchi')):
        if (message.channel.nsfw==True):
            # These are only allowed by 18+ Role
            if 'busta' in message.content.lower():
                await message.channel.send('bust-a-nut')
            
            if message.content.startswith(command_prefix[0]+'ecchi'):
                __count_statistics__(serverlist,message.guild.id,'ecchi_command')
                botcount+=1
                ecchi_vote = True
                await message.add_reaction('😏')
                methods=['joyreactor','imgbin','img2wall','src3']
                a=choice(methods)

                if a=='joyreactor':
                    joyreactor()
                    x=joyreactor()
                    embed = discord.Embed(title=f"**Joyreactor Source**", description=f"Requested by {message.author.mention}", colour=discord.Colour(0xa779ff), url=x)
                    embed.set_image(url=x)
                    embed.set_footer(text=f"🔞 Courtsey of TemperatureWash", icon_url=client.user.avatar_url)
                    await message.channel.send(embed=embed)

                elif(a=='imgbin'):
                    imgbin()
                    x=imgbin()
                    embed = discord.Embed(title=f"**Imgbin Source**",description=f"Requested by {message.author.mention}", colour=discord.Colour(0xa779ff), url=x)
                    embed.set_image(url=x)
                    embed.set_footer(text=f"🔞 Courtsey of TemperatureWash", icon_url=client.user.avatar_url)
                    await message.channel.send(embed=embed)
                elif(a=='img2wall'):
                    img2wall()
                    x=img2wall()
                    embed = discord.Embed(title=f"**Img2Wall Source**",description=f"Requested by {message.author.mention}", colour=discord.Colour(0xa779ff), url=x)
                    embed.set_image(url=x)
                    embed.set_footer(text=f"🔞 Courtsey of TemperatureWash", icon_url=client.user.avatar_url)
                    await message.channel.send(embed=embed)
                elif(a=='src3'):
                    src3()
                    x=src3()
                    embed = discord.Embed(title=f"**Src3's Source**", description=f"Requested by {message.author.mention}", colour=discord.Colour(0xa779ff), url=x)
                    embed.set_image(url=x)
                    embed.set_footer(text=f"🔞 Courtsey of TemperatureWash", icon_url=client.user.avatar_url)
                    await message.channel.send(embed=embed)
                __count_statistics__(serverlist,message.guild.id,'ecchi_command')
        else:
            ecchi_vote = False
            await message.add_reaction('😒')
            await message.channel.send(choice(perks['replies']['nsfw_error']))
            await message.channel.send(choice(perks['links']['nsfw_error']))

    
    if('nice' in str(message.content).lower().replace(' ','') or 'noice' in str(message.content).lower().replace(' ','') and str(message.channel.name) == "cursed-by-shriram"):
        await message.channel.send(r'( ͡° ͜ʖ ͡°)')
        __count_statistics__(serverlist,message.guild.id,'nice')
    
    if(message.content.startswith(command_prefix[0]+'emoji')):
        emname = message.content[6:].replace(' ','')

        for ej in client.emojis:
            if(ej.name == emname):
                serverlist[str(message.guild.id)] = {'emoji':emname}
                await message.add_reaction('✔')


                embed=discord.Embed(color=0x00ff00)
                embed.add_field(name="Emoji Updated", value="emoji has been updated", inline=False)
                embed.set_footer(text="love from echan")
                await message.channel.send(embed=embed)
                break

        if(str(message.channel.name) == "cursed-by-darkness"):
            for role in message.author.roles:
                if(role.name == "smolpp"):
                    await message.add_reaction('🤏')
                    await message.add_reaction('🍆')

            if(str(message.guild.id) in serverlist):
                for ej in client.emojis:
                    if(ej.name == serverlist[str(message.guild.id)]['emoji'] and str(ej.guild.id) == str(message.guild.id)):
                        await message.add_reaction(ej)  

            elif(not message.guild.id in serverlist):
                await message.add_reaction('❌')


client.run('REWRITE') #REMOVE TOKEN