from time import *
from random import *
import time,subprocess,discord,os
import numpy as np

client = discord.Client()
darkemoji = None
channel = "760509524833599539"
client = discord.Client()
emojiname='darkalpha'

@client.event
async def on_ready():
    global darkemoji,client
    print('We have logged in as {0.user}'.format(client))
    statustxt = "Dark is daddy"
    activity = discord.Game(name=statustxt)
    for ej in client.emojis:
        if(ej.name == emojiname):
            darkemoji = ej
            print("emoji found!")
    await client.change_presence(status=discord.Status.online, activity=activity)



@client.event
async def on_message(message):
    global darkemoji,client,channel
    if message.author == client.user:
        return
   
        
        
    
    if(str(message.channel.id) == "760509524833599539"):
        for role in message.author.roles:
            if(role.name == "smolpp"):
                print("yes he has small pp")
                await message.add_reaction('🤏')
                await message.add_reaction('🍆')
        await message.add_reaction(darkemoji)
    if (message.channel.nsfw==True):
        if message.content.startswith('-ecchi'):
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
                
        if 'good-bot' in message.content.lower():
             await message.channel.send('thank you master i shall pleasure you for eternity')
        if 'busta' in message.content.lower():
            await message.channel.send('bust-a-nut')
        if 'echo' in message.content.lower():
            await message.channel.send(message.content[5:len(message.content)])
        if  message.content.startswith('!python'):
            import subprocess
            x=message.content[7:]
            p = subprocess.run('''python "{0}"'''.format(x), capture_output=True, shell=True)
            await message.channel.send((p.stdout.decode(),p.stderr.decode()))
    


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
client.run('<token>')
