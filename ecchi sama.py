from time import *
from random import *
import time,subprocess,discord,os, mal
import numpy as np


# REMOVE TOKEN BEFORE COMMITTING CHANGES


client = discord.Client()
darkemoji = None
client = discord.Client()
emojiname='darkalpha' #defaulted emojiname
anime_reply = False
botcount = 0
currentcount = 0

d_token = open(r"D:\Downloads\bot.token",'r').readlines()[0]

debugchat = False
serverlist = {'705682250460823602': {'emoji': 'blackaus' , 'debug':1 }, '433901628018655232': {'emoji': 'sus' , 'debug':0 }, '685469328929587268': {'emoji': 'kikiangry' , 'debug':0 }}


#additional variables
ecchi_vote = False
bad_person = ['This isnt an NSFW Channel :/','Kids are in this server shhhh','Look where you texting ... this aint NSFW','So you want "Pixels fucking pixels" ~ LeoJesvyn huh','This is only supposed to be used in NSFW channels']
irumalinks = [
    'https://static.wikia.nocookie.net/mairimashita-irumakun/images/c/c9/Iruma_Suzuki.png/revision/latest?cb=20191217095641',
    'https://www.monstersandcritics.com/wp-content/uploads/2019/12/Welcome-to-Demon-School-Iruma-kun-Season-2-release-date-Mairimashita-Iruma-kun-manga-compared-to-the-anime.jpg',
    'https://static.wikia.nocookie.net/mairimashita-irumakun/images/b/b9/WickedIruma.png/revision/latest?cb=20200430234437',
    'https://spoilerguy.com/wp-content/uploads/2020/02/Welcome-to-Demon-School-Iruma-kun-Episode-19.jpg',
    'https://i.ytimg.com/vi/kXmUWo7jTdk/maxresdefault.jpg',
    'https://simkl.net/episodes/88/8887367035de32433_w.jpg',
    'https://media1.tenor.com/images/e17290e12dc0f60ab3021e100fa33438/tenor.gif?itemid=15870136',
    'https://64.media.tumblr.com/60aabf00e266eae4253fcdaf60076d49/tumblr_pywk6pYme91v6bs4yo4_r1_250.gifv',
    'https://media.discordapp.net/attachments/757838382419279903/760583834764181554/318964034116201.png'
]

@client.event
async def on_ready():
    global darkemoji,client
    print('We have logged in as {0.user}'.format(client))
    statustxt = "with irumachi's pp"
    activity = discord.Game(name=statustxt)
    await client.change_presence(status=discord.Status.online, activity=activity)



@client.event
async def on_message(message):
    global darkemoji,client,channel,ecchi_vote,botcount,serverlist,debugchat,currentcount
    if message.author == client.user:
        if(ecchi_vote):
            await message.add_reaction('⬆')
            await message.add_reaction('⬇')
            ecchi_vote = False
        return

        '''
            if(message.content.startswith('>')):
                pass #removed due to discord api restrictions
        '''                    
                
 

# Perks from Pacchu :D
    if(message.content.startswith('-debug')):
        if(not debugchat):
            debugchat = True
            embed=discord.Embed(color=0x00ff00)
            embed.add_field(name="DEBUG", value="ENABLED", inline=False)
            await message.channel.send(embed=embed)
        elif(debugchat):
            debugchat = False
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="DEBUG", value="DISABLED", inline=False)
            await message.channel.send(embed=embed)        

    if(str(message.channel.name) == "cursed-by-shriram"):
        for role in message.author.roles:
            if(role.name == "smolpp"):
                print("yes he has small pp")
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
                            embed.set_footer(text="Debug window")
                            await message.channel.send(embed=embed)

                     

        elif(not message.guild.id in serverlist):
            await message.add_reaction('❌')
            if(debugchat):
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="Emoji not found", value="Consider setting server reaction emoji using -emoji emojiname", inline=False)
                embed.set_footer(text="result 404")
                await message.channel.send(embed=embed)
                
        
    if(message.content.startswith('-status')):
        newstatus = str(message.content)[7:]
        activity = discord.Game(name=newstatus)
        await message.channel.send(f'Changed status to **Playing {newstatus}**')
        await message.add_reaction('💗')
        await client.change_presence(status=discord.Status.online, activity=activity)
        
    if(message.content.startswith('-help')):
        embed=discord.Embed(color=0xff00bb)
        embed.set_thumbnail(url="http://i.redd.it/5xkpkqjoz9g11.jpg")
        embed.add_field(name="echan", value="Echan help", inline=False)
        embed.add_field(name="-irumachi", value="Sends a Shriram approved photo of Irumakun :D", inline=False)
        embed.add_field(name="-status newstatus", value="changes status of the bot", inline=False)
        embed.add_field(name="-bruh", value="bruh", inline=False)

        if (message.channel.nsfw==True):
            embed.add_field(name="-recchi", value="gets latest r/ecchi post from reddit [ COMMING SOON ]", inline=False)
            embed.add_field(name="-ecchi", value="sends a random nsfw image", inline=False)
            embed.add_field(name="-hentai", value="Suggests a random hentai from database", inline=False)
            embed.add_field(name="-sauce", value="sends source of image [ COMMING SOON ]", inline=False)
            embed.add_field(name="-upload link", value="send newds wink [ COMMING SOON ;) ]", inline=False)
            embed.add_field(name="-stats", value="Check who used ecchibot alot", inline=False)
        else:
            embed.add_field(name="-------", value="6 NSFW commands hidden", inline=False)

        embed.add_field(name="-perks", value="Lists the perks of this bot", inline=False)
        embed.add_field(name="-help", value="bruh this is exactly the same command you ran", inline=False)
        embed.set_footer(text="Love from echan ")
        await message.channel.send(embed=embed)

    if(message.content.startswith('-perks')):
        embed=discord.Embed(title="EcchiChan", description="Ecchi perks ", color=0xff9500)
        embed.set_thumbnail(url="https://i.redd.it/5xkpkqjoz9g11.jpg")
        embed.add_field(name="Emote spammer", value=f"Spams {emojiname} emote in #cursed-by-dark", inline=False)
        embed.add_field(name="Nice Lenny", value=f"searches for nice or noice in messages", inline=False)
        embed.set_footer(text="with love from ecchichan")
        await message.channel.send(embed=embed)

    if(message.content.startswith('-irumachi')):
        await message.channel.send(choice(irumalinks))

    if(message.content.startswith("-anime")):
        asrc = [" "]
        animestr = str(message.content)[6:]
        try:
            asrc = mal.AnimeSearch(animestr).results
            embed=discord.Embed(title=asrc[0].title, description=f"[{asrc[0].type}]")
            embed.set_author(name=asrc[0].title)
            embed.set_thumbnail(url=asrc[0].image_url)
            embed.add_field(name="Rating", value=asrc[0].score, inline=False)
            embed.add_field(name="Episodes", value=asrc[0].episodes, inline=True)
            embed.add_field(name="Synopsis", value=asrc[0].synopsis, inline=True)
            embed.set_footer(text="data from Pacchu's slave bot")
            await message.channel.send(embed=embed)


        except ValueError:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="Whoops", value="Unable to find anime with that name", inline=False)
            embed.set_footer(text="result 404")
            await message.channel.send(embed=embed)

    if(message.content.startswith('-bruh')):
        await message.channel.send("https://media.discordapp.net/attachments/760741167876538419/760744075132534784/DeepFryer_20200930_113458.jpg?width=448&height=518")

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


    #Temporary use of MyAnimeList until Manbonpan adds his own API implementation

    if(message.content.startswith("-anime")):
        asrc = [" "]
        animestr = str(message.content)[6:]
        try:
            asrc = mal.AnimeSearch(animestr).results
            embed=discord.Embed(title=asrc[0].title, description=f"[{asrc[0].type}]")
            embed.set_author(name=asrc[0].title)
            embed.set_thumbnail(url=asrc[0].image_url)
            embed.add_field(name="Rating", value=asrc[0].score, inline=False)
            embed.add_field(name="Episodes", value=asrc[0].episodes, inline=True)
            embed.add_field(name="Synopsis", value=asrc[0].synopsis, inline=True)
            embed.set_footer(text="data scraped from myanimelist")
            anime_flag = False
            await message.channel.send(embed=embed)
            

        except ValueError:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="Anime Not Found", value="That Anime is not found on MyAnimeList", inline=False)
            await message.channel.send(embed=embed)
    
    # End of temp function
    

    #Upcomming 

    if('nice' in str(message.content).lower().replace(' ','') or 'noice' in str(message.content).lower().replace(' ','') and str(message.channel.name) == "cursed-by-shriram"):
        await message.channel.send(r'( ͡° ͜ʖ ͡°)')
        if(debugchat):
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="DEBUG", value="noice found", inline=False)
                await message.channel.send(embed=embed)

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
        embed.set_footer(text="Feature_Not_Defined")
        await message.channel.send(embed=embed)
    
    if(message.content.startswith('-hentai')):
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="COMMING SOON", value="function not defined", inline=False)
        embed.set_footer(text="Feature_Not_Defined")
        await message.channel.send(embed=embed)
    
    if(message.content.startswith('-stats')):
        embed=discord.Embed(color=0xff0000)
        embed.add_field(name="Bot summons", value=f"This bot was summoned {botcount} times", inline=False)
        embed.set_footer(text="With love from echan")
        await message.channel.send(embed=embed)
        if(debugchat):
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="DEBUG", value="This command is a debug command basically", inline=False)
                await message.channel.send(embed=embed)
        
        

# Backend by TemperatureBlock :D


    if (message.channel.nsfw==True):
        for role in message.author.roles:
            if(role.name == "18+"):
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

                    elif a=='imgbin':
                        imgbin()
                        x=imgbin()
                        await message.channel.send(x)
                    elif a=='img2wall':
                        img2wall()
                        x=img2wall()
                        await message.channel.send(x)
                    elif a=='src3':
                        src3()
                        x=src3()
                        await message.channel.send(x)
     
    # Anyone can use these commands now :D
    if 'good-bot' in message.content.lower():
         await message.channel.send(f'ありがとう {message.author.name} i shall pleasure you for eternity')
    if 'echo' in message.content.lower():
        await message.channel.send(message.content[5:len(message.content)])
    if  message.content.startswith('!python'):
        import subprocess
        x=message.content[7:]
        p = subprocess.run('''python "{0}"'''.format(x), capture_output=True, shell=True)
        await message.channel.send((p.stdout.decode(),p.stderr.decode()))
    else:
        if message.content.startswith('-ecchi'):
            ecchi_vote = False
            await message.add_reaction('😒')
            await message.channel.send(choice(bad_person))
            await message.channel.send('https://toxicmuffin.files.wordpress.com/2016/06/kono-subarashi-sekai-ni-shukufuku-wo-22.jpg')



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

client.run('TOKEN')
