from time import *
from random import *
import time,subprocess,discord,os,json,io
from jikanpy import Jikan
import numpy as np
import urllib3

jsonfile = io.open("perks.json",mode="r",encoding="utf-8")

# REMOVE TOKEN BEFORE COMMITTING CHANGES Dont forget pls
http = urllib3.PoolManager()
anime = Jikan() #new ANIME API
client = discord.Client()
darkemoji = None
client = discord.Client()
emojiname='darkalpha' #defaulted emojiname
anime_reply = False
botcount = 0
currentcount = 0
asrc = ['']
prefix = ''


debugchat = False
serverlist = {'default' : {'emoji':'🌊','debug':0,'bruh':'https://media.discordapp.net/attachments/760741167876538419/760744075132534784/DeepFryer_20200930_113458.jpg?width=448&height=518'},'705682250460823602': {'emoji': 'blackaus' , 'debug':1 , 'bruh':'https://media.discordapp.net/attachments/760741167876538419/760744075132534784/DeepFryer_20200930_113458.jpg?width=448&height=518' }, '433901628018655232': {'emoji': 'sus' , 'debug':0 }, '685469328929587268': {'emoji': 'kikiangry' , 'debug':0 }}
perks = json.load(jsonfile)

#additional variables
ecchi_vote = False

def list_to_string(the_list,no_of_items:int):
    returnstr = ''
    count = 0
    for _ in the_list:
        if(count > no_of_items):
            break
        count+= 1
        returnstr += str(_ + "\n")
    return returnstr


@client.event
async def on_ready():
    global darkemoji,client
    print('We have logged in as {0.user}'.format(client))
    statustxt = "Running in sorta Confident mode :D"
    activity = discord.Game(name=statustxt)
    await client.change_presence(status=discord.Status.online, activity=activity)



@client.event
async def on_message(message):
    global darkemoji,client,channel,ecchi_vote,botcount,serverlist,debugchat,currentcount,asrc,http
    pacchu_user = client.get_user(int("170783707647442947"))
    temp_user = client.get_user(int("569911088141959189"))
    if message.author == client.user:
        if(ecchi_vote):
            await message.add_reaction('⬆')
            await message.add_reaction('⬇')
            ecchi_vote = False
        return

    for x in message.mentions:
        if(x==client.user):
            await message.channel.send(choice(perks['replies']['pings']) + message.author.mention)
    
    
    if(message.content.startswith('-hug')):
        hug_person = str(message.content)[8:-1]
        hgp = client.get_user(int(hug_person))
        await message.add_reaction('🤗')
        if(message.author == hgp  or hgp == None):
            embed = discord.Embed(title=" ",description=f"{message.author.mention} hugs themselves", colour=discord.Colour(0xcd94ff))
            embed.add_field(name="😢", value=f"Don't worry {message.author.mention}.. {choice(perks['replies']['sadhugs'])}")
            embed.set_image(url=choice(perks['links']['sadhugs']))
        else:
            embed = discord.Embed(title=" ",description=f"{message.author.mention} hugs {hgp.mention}", colour=discord.Colour(0xcd94ff))
            embed.set_image(url=choice(perks['links']['hugs']))

        embed.set_thumbnail(url=hgp.avatar_url)
        embed.set_author(name=" ", icon_url=message.author.avatar_url)
        embed.set_footer(text=f"with love from {client.user.name} :)", icon_url=client.user.avatar_url)
        await message.channel.send(embed=embed)
        return
    
    if(message.content.startswith('-avatar')):
        hug_person = str(message.content)[11:-1]
        hgp = client.get_user(int(hug_person))
        await message.add_reaction('👌')
        if(message.author == hgp  or hgp == None):
            embed = discord.Embed(title=" ",description=f"{message.author.mention} steals ...wait thats your OWN", colour=discord.Colour(0xcd94ff))
            embed.set_image(url=message.author.avatar_url)
        else:
            embed = discord.Embed(title=" ",description=f"{message.author.mention} steals {hgp.mention}'s profile pic 👀'", colour=discord.Colour(0xcd94ff))
            embed.set_image(url=hgp.avatar_url)
        embed.set_footer(text=f"with love from {client.user.name} :)", icon_url=client.user.avatar_url)
        await message.channel.send(embed=embed)
        return
    
    
    if(message.content.startswith('-kiss')):
        hug_person = str(message.content)[9:-1]
        hgp = client.get_user(int(hug_person))
        print(hug_person)
        await message.add_reaction('🤗')
        if(message.author == hgp  or hgp == None):
            embed = discord.Embed(title=" ",description=f"{message.author.mention} kisses themselves", colour=discord.Colour(0xcd94ff))
            embed.add_field(name="👀", value=f"HOW!!!?")
            embed.set_image(url=choice(perks['links']['erotic_perv']))
        else:
            embed = discord.Embed(title=" ",description=f"{message.author.mention} kisses {hgp.mention}", colour=discord.Colour(0xcd94ff))
            embed.set_image(url=choice(perks['links']['kiss']))

        embed.set_thumbnail(url=hgp.avatar_url)
        embed.set_author(name=" ", icon_url=message.author.avatar_url)
        embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
        await message.channel.send(embed=embed)

    if(message.content.startswith('-pat')):
        hug_person = str(message.content)[8:-1]
        hgp = client.get_user(int(hug_person))
        await message.add_reaction('🤗')
        if(message.author == hgp or hgp == None):
            embed = discord.Embed(title=" ",description=f"{message.author.mention} pats themselves", colour=discord.Colour(0xcd94ff))
            embed.add_field(name="👋", value=f"{message.author.mention}.. i'll pat you :3")
            embed.set_image(url=choice(perks['links']['pats']))
        else:
            embed = discord.Embed(title=" ",description=f"{message.author.mention} pats {hgp.mention}", colour=discord.Colour(0xcd94ff))
            embed.set_image(url=choice(perks['links']['pats']))

        embed.set_thumbnail(url=hgp.avatar_url)
        embed.set_author(name=" ", icon_url=message.author.avatar_url)
        embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
        await message.channel.send(embed=embed)

# Perks from Pacchu :D

    if(str(message.channel.name) == "cursed-by-darkness"):
        for role in message.author.roles:
            if(role.name == "smolpp"):
                await message.add_reaction('🤏')
                await message.add_reaction('🍆')
        


        if(str(message.guild.id) in serverlist):
            for ej in client.emojis:
                if(ej.name == serverlist[str(message.guild.id)]['emoji'] and str(ej.guild.id) == str(message.guild.id)):
                    await message.add_reaction(ej)  
                    if(debugchat):
                            embed=discord.Embed(color=0x00ff00)
                            embed.add_field(name="Guild ID", value=message.guild.id, inline=False)
                            embed.add_field(name="Guild Emoji set", value=serverlist[str(message.guild.id)]['emoji'], inline=False)
                            embed.add_field(name="Emoji Guild ID", value=str(ej.guild.id), inline=False)
                            embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
                            await message.channel.send(embed=embed)


                     

        elif(not message.guild.id in serverlist):
            await message.add_reaction('❌')
            if(debugchat):
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="Emoji not found", value="Consider setting server reaction emoji using -emoji emojiname", inline=False)
                embed.set_footer(text=f"404 ;)", icon_url=client.user.avatar_url)
                await message.channel.send(embed=embed)
                
        
    if(message.content.startswith('-status')):
        newstatus = str(message.content)[7:]
        activity = discord.Game(name=newstatus)
        await message.channel.send(f'Changed status to **Playing {newstatus}**')
        await message.channel.send(f'_💀 This is visible in all the servers the bot is in_')
        await message.add_reaction('✋')
        await client.change_presence(status=discord.Status.online, activity=activity)
        




    ## HELP COMMAND <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    if(message.content.startswith('-help')):
        embed=discord.Embed(color=0xae00ff,description=f"Created by Pacchu and TemperatureWash")
        embed.set_thumbnail(url="http://i.redd.it/5xkpkqjoz9g11.jpg")
        embed.add_field(name="How can I help you", value="echan commands", inline=False)
        embed.add_field(name="-anime", value="Searches for given anime", inline=True)
        embed.add_field(name="-manga", value="Searches for give Manga", inline=True)
        embed.add_field(name="-anichar", value="Searches for given Anime Charactor [BETA] ", inline=True)
        embed.add_field(name="-anipics", value="Searches for Images of given Anime Charactor [ALPHA] ", inline=True)
        embed.add_field(name="-avatar <person>", value="Steals the person's DP :d", inline=False)
        embed.add_field(name="-status newstatus", value="changes status of the bot", inline=False)
        embed.add_field(name="-bruh", value="bruh", inline=False)


        if (message.channel.nsfw==True):
            embed.add_field(name="NSFW COMMANDS", value="18+", inline=False)
            embed.add_field(name="-recchi", value="gets latest r/ecchi post from reddit [ COMMING SOON ]", inline=False)
            embed.add_field(name="-ecchi", value="sends a random nsfw image", inline=False)
            embed.add_field(name="-hentai", value="Suggests a random hentai from database [ COMMING SOON ]", inline=False)
            embed.add_field(name="-stats", value="Check who used ecchibot alot", inline=False)

            #Completely Hiding NSFW Commands

        embed.add_field(name="-irumachi", value="Sends an Adorable photo of irumakun from Marimashita irumakun", inline=False)
        embed.add_field(name="-perks", value="Lists the perks of this bot", inline=False)
        embed.add_field(name="-help", value="isnt it obvious :o", inline=False)

        embed.set_footer(text=f"I am {client.user.name} v0.4 alpha", icon_url=client.user.avatar_url)
        await message.channel.send(embed=embed)
        return



     ## PERKS COMMAND <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    if(message.content.startswith('-perks')):
        embed=discord.Embed(title="EcchiChan", description="Ecchi perks ", color=0xff9500)
        embed.set_thumbnail(url="https://i.redd.it/5xkpkqjoz9g11.jpg")
        embed.add_field(name="Emote spammer", value=f"Spams {emojiname} emote in #cursed-by-dark", inline=False)
        embed.add_field(name="Nice Lenny", value=f"searches for nice or noice in messages", inline=False)
        embed.add_field(name="Ping Awareness", value=f"I Know when you ping me", inline=False)
        embed.set_footer(text=f" {client.user.name} v0.4 alpha", icon_url=client.user.avatar_url)
        await message.channel.send(embed=embed)
        return

    if(message.content.startswith('-irumachi')):
        await message.channel.send(choice(perks["links"]["iruma"]))
        return

    if(message.content.startswith('-bruh')):
        after = message.content[5:]
        if(message.content == '-bruh'):
            try:
                await message.channel.send(serverlist[str(message.guild.id)]['bruh'])
            except KeyError:
                await message.channel.send(serverlist['default']['bruh'])
        else:
            serverlist[str(message.guild.id)] = {'bruh':after}
            embed=discord.Embed(color=0x00ff00)
            embed.add_field(name="Bruh image Updated", value="Bruh image has been sucessfully updated", inline=False)
            embed.set_footer(text=f" {client.user.name} v0.4 alpha", icon_url=client.user.avatar_url)
            await message.channel.send(embed=embed)
        return


    if(message.content.startswith('-emoji')):
        emname = message.content[6:].replace(' ','')
        if(debugchat):
                embed=discord.Embed(color=0xffffff)
                embed.add_field(name="DEBUG", value=f"Searching for emoji named {emname}", inline=False)
                await message.channel.send(embed=embed)

        for ej in client.emojis:
            if(ej.name == emname):
                serverlist[str(message.guild.id)] = {'emoji':emname}
                await message.add_reaction('✔')


                embed=discord.Embed(color=0x00ff00)
                embed.add_field(name="Emoji Updated", value="emoji has been updated", inline=False)
                embed.set_footer(text="love from echan")
                await message.channel.send(embed=embed)

                if(debugchat):
                    embed=discord.Embed(color=0x00ff00)
                    embed.add_field(name="DEBUG", value=serverlist, inline=False)
                    await message.channel.send(embed=embed)
                
                break
        return


   ### ANIME RELATED STUFF 
    
    if(message.content.startswith("-anichar")):
        anicharstr = str(message.content)[8:]
        try:
            await message.add_reaction('😉')
            asrc = anime.character(anime.search('Character ',anicharstr)['results'][0]['mal_id'])
            embed = discord.Embed(title=f"**{asrc['name']}**", colour=discord.Colour(0xa779ff), url=asrc['url'], description=asrc['about'][:512].strip()+'...')
            embed.set_image(url=asrc['image_url'])
            embed.set_footer(text=f"Not the correct Character ... Try spelling their full name", icon_url=client.user.avatar_url)
            embed.add_field(name="Waifu/Husbando-Meter", value=f"{asrc['member_favorites']} have liked them", inline=False)
            await message.channel.send(embed=embed)
        except:
            await message.add_reaction('😞')
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="Character Not Found", value="That Character is not found ", inline=False)
            embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
            await message.channel.send(embed=embed)
        return
    
    if(message.content.startswith("-anipics")):
        anicharstr = str(message.content)[8:]
        try:
            await message.add_reaction('😉')
            charid = anime.search('character',anicharstr)['results'][0]
            url = f"https://api.jikan.moe/v3/character/{charid['mal_id']}/pictures"
            picdat = json.loads(http.request('GET',url).data.decode())['pictures']
            embed = discord.Embed(title=f"**{charid['name']}**", colour=discord.Colour(0xa779ff), url=charid['url'])
            embed.set_image(url=choice(picdat)['small'])
            embed.set_footer(text=f"Not the correct charector... Try spelling their full name", icon_url=client.user.avatar_url)
            await message.channel.send(embed=embed)
        except:
            await message.add_reaction('😞')
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="Images Not Found", value=" Coudn't find any images on given Query ", inline=False)
            embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
            await message.channel.send(embed=embed)
        return



    if(message.content.startswith("-anime")):
        asrc = [" "]
        animestr = str(message.content)[6:]
        try:
            await message.add_reaction('😉')
            start = time.time()
            asrc = anime.search('anime',animestr)['results'][0]
            end = time.time()
            mal_id = asrc['mal_id']
            more_info = anime.anime(mal_id)
            
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
            await message.channel.send(embed=embed)

            

        except:
            await message.add_reaction('😭')
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="Anime Not Found", value="That Anime is not found on MyAnimeList", inline=False)
            embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
            await message.channel.send(embed=embed)
        return


    if(message.content.startswith("-manga")):
        asrc = [" "]
        mangastr = str(message.content)[6:]
        try:
            start = time.time()
            asrc = anime.search('manga',mangastr)['results'][0]
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
            await message.channel.send(embed=embed)
            

        except:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="Manga Not Found", value="That manga was not found on MyAnimeList.. webtoons are not yet supported", inline=False)
            await message.channel.send(embed=embed)
        return

   

    ### END OF ANIME RELATED STUFF

    if('nice' in str(message.content).lower().replace(' ','') or 'noice' in str(message.content).lower().replace(' ','') and str(message.channel.name) == "cursed-by-shriram"):
        await message.channel.send(r'( ͡° ͜ʖ ͡°)')
        if(debugchat):
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="DEBUG", value="noice found", inline=False)
                await message.channel.send(embed=embed)


    #Upcomming 

    if(message.content.startswith('-sauce')):
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="COMMING SOON", value="function not defined", inline=False)
        embed.set_footer(text="Feature_Not_Defined")
        await message.channel.send(embed=embed)
        if(debugchat):
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="DEBUG", value="function not available", inline=False)
                await message.channel.send(embed=embed)

    if(message.content.startswith('-upload')):
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="COMMING SOON", value="function not defined", inline=False)
        embed.set_footer(text="Feature_Not_Defined",icon_url=client.user.avatar_url)
        await message.channel.send(embed=embed)
    
    if(message.content.startswith('-hentai')):
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="COMMING SOON", value="function not defined", inline=False)
        embed.set_footer(text="Feature_Not_Defined")
        await message.channel.send(embed=embed)
    
    if(message.content.startswith('-stats')):
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="Bot summons", value=f"This bot was summoned {botcount} times", inline=False)
        embed.set_footer(text=f"with love from {client.user.name} ;)", icon_url=client.user.avatar_url)
        await message.channel.send(embed=embed)
        if(debugchat):
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="DEBUG", value="This command is a debug command basically", inline=False)
                await message.channel.send(embed=embed)
        
        

# Backend by TemperatureBlock :D


    if (message.channel.nsfw==True):
        # These are only allowed by 18+ Role
        if 'busta' in message.content.lower():
            await message.channel.send('bust-a-nut')
        if message.content.startswith('-ecchi'):
            botcount+=1
            ecchi_vote = True
            await message.add_reaction('😏')
            methods=['joyreactor','imgbin','img2wall','src3']
            a=choice(methods)

            if a=='joyreactor':
                joyreactor()
                x=joyreactor()
                await message.channel.send(x)

            elif(a=='imgbin'):
                imgbin()
                x=imgbin()
                await message.channel.send(x)
            elif(a=='img2wall'):
                img2wall()
                x=img2wall()
                await message.channel.send(x)
            elif(a=='src3'):
                src3()
                x=src3()
                await message.channel.send(x) 
    else:
        if message.content.startswith('-ecchi'):
            ecchi_vote = False
            await message.add_reaction('😒')
            await message.channel.send(choice(perks['replies']['nsfw_error']))
            await message.channel.send(choice(perks['links']['nsfw_error']))

    if 'good-bot' in message.content.lower():
         await message.channel.send(f'ありがとう {message.author.name} i shall pleasure you for eternity')
    if 'echo' in message.content.lower():
        await message.channel.send(message.content[5:len(message.content)])

    



###############################################################################
def joyreactor():
    f = open("joyreactor(REDONE).bin.npy","rb")
    aa = np.load(f,allow_pickle = True)
    aaa=choice(aa)
    return aaa
###############################################################################

def imgbin():
    f = open("imgbin.bin.npy","rb")
    aa = np.load(f,allow_pickle = True)
    aaa=choice(aa)
    return aaa
################################################################################

def img2wall():
    f = open("links2wall.bin.npy","rb")
    aa = np.load(f,allow_pickle = True)
    aaa=choice(aa)
    return aaa
################################################################################
def src3():
    f = open("src3.bin.npy","rb")
    aa = np.load(f,allow_pickle = True)
    aaa=choice(aa)
    return aaa
################################################################################
#token = str(d_token.readline()[0])

client.run('MEGU') #i keep forgetting to remove this thing
