#deprecated by mongo db ill remove it later

from __future__ import print_function
import binascii
import struct
from PIL import Image
from discord import colour
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import urllib3,os
import requests
from tqdm import tqdm
from . import __imports__ as internalImports


lifeChoice = [True,False]

botReadyToRespond = True

async def report_errors_to_channel(client,error):
    pass
    """print(repr(error))
    channel = await client.get_channel(501237046854287365)
    await client.send(f"```{str(repr(error))}```")"""
    

distortionTypes = [lambda i, j:[2*np.sin(i/100) + 2, 2*np.sin(j/100) + 2],
                   lambda i, j:[2*np.sin(i/100) + 2, 0],
                   lambda i, j:[0, 4*np.sin(j/100) + 4],
                   lambda i, j:[abs(np.tan(i/100)), np.cos(j/100) + 2],
                   lambda i, j:[4*np.tan(i/100), 0],
                   lambda i, j:[0, 4*np.tan(j/100)],
                   lambda i, j: [1*np.sin(i/100), 1*np.cos(j/100)],
                   ]


async def ButtonProcessor(ctx,res,label:str,userCheck=True):
    try:
        if(res.component.label == label):
            if(res.author.id == ctx.author.id or not userCheck):
                return True
            else:
                await res.respond(
                    type=internalImports.InteractionType.ChannelMessageWithSource,
                    content="Only the person who requested can do that mate"
                )
                return False
    except:
        await res.respond(
            type=internalImports.InteractionType.ChannelMessageWithSource,
            content="That Button expired mate"
        )
        return False
        
async def unified_imagefetcher(ctx,member=None,attachedImg=None):
    await ctx.message.add_reaction('🖌')
    try:
        if(attachedImg == None):
            attachment_url = ctx.message.attachments[0].url
        else:
            attachment_url = attachedImg
        await ctx.message.add_reaction('📩')
        await ctx.send("Downloading and processing image 📩")
        return attachment_url
    except:
        try:
            hgp = member
            await ctx.message.add_reaction('🎭')
            if(ctx.message.author == hgp or hgp == None):
                attachment_url = ctx.message.author.avatar_url
            else:
                attachment_url = hgp.avatar_url
            await ctx.send("Getting User's avatar")
            return attachment_url
        except:
            await ctx.send("> I think something went wrong!")
            return None

def ButtonValidator(res,ctx,userCheck=False):
    cond = (res.channel == ctx.channel)
    if(userCheck):
        cond = cond and (res.author.id==ctx.author.id)
    return cond


def find_dominant_color(imageurl:str,local=False):
    try:
        NUM_CLUSTERS = 10
        if(local):
            im = Image.open(imageurl)
        else:
            im = Image.open(requests.get(imageurl, stream=True).raw)
        im = im.resize((25, 25))    
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        vecs, dist = scipy.cluster.vq.vq(ar, codes)        
        counts, bins = scipy.histogram(vecs, len(codes))   
        index_max = scipy.argmax(counts)                   
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        try:
            return int(hex(int(colour, 16))[:8], 0)
        except:
            return  0xffffff
    except IndexError:
        return 0xffffff

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

bot_avatar_url = "https://cdn.discordapp.com/attachments/715107506187272234/850379532459573288/pacslav.png"


def mentionToId(mention:str):
    print(mention)
    return int(mention[3:-1])


def queryToName(var):
    name = ""
    for _ in var:
        name += " " + _
    return name

def list_to_string(the_list,no_of_items:int):
    returnstr = ''
    count = 0
    for _ in the_list:
        if(count > no_of_items):
            break
        count+= 1
        returnstr += str(_ + "\n")
    return returnstr

def embed_generator(embedContents,thumbUrl,imgUrl):
    pass

def get_file_or_link(ctx,qlink=None):
    try:
        return ctx.message.attachments[0].url
    except:
        if('http' in ctx.message.content or 'https' in ctx.message.content):
            return queryToName(qlink)
        else:
            return ctx.message.author.avatar_url

def better_send(ctx,content=None,embed=None,file=None):
    try:
        try:
            return ctx.reply(content, embed=embed, file=file)
        except:
            return ctx.send(content, embed=embed, file=file)
    except:
        return ctx.send("Coudn't send the message.. something went wrong!!")


def isItPacchu(checkid:str):
    #                   Pacchu              Pacchu              Macky            Leo                Monsieur
    return checkid in [749975627633000520,170783707647442947,741139834260815964,520114282776625162,627135815985659904]


def domain_finder(link):
    import string
    dot_splitter = link.split('.')

    seperator_first = 0
    if '//' in dot_splitter[0]:
        seperator_first = (dot_splitter[0].find('//') + 2)

    seperator_end = ''
    for i in dot_splitter[2]:
        if i in string.punctuation:
            seperator_end = i
            break

    if seperator_end:
        end_ = dot_splitter[2].split(seperator_end)[0]
    else:
        end_ = dot_splitter[2]

    domain = [dot_splitter[0][seperator_first:], dot_splitter[1], end_]
    domain = '.'.join(domain)

    return domain


class Emotes:
    PACPILOVE = "<:pacpilove:860277910106800198>"
    PACCHU = "<:pacchu:860277741546373131>"
    PACEXCLAIM = "<:pacDoubleExclaim:858677949775872010>"
    PACSTOP = '<:pacstop:860273983614091325>'
    PACPLAY = '<:pacplay:860273984213483531>'
    PACPAUSE = '<:pacpause:860273984218464267>'
    PACDEPRESS = "<:pacdepression:860277067730649135>"
    LOFISPARKO = "<:lofisparko:858551929977962547>"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEFAULT = CGREY  = '\33[90m'
    CWHITE2  = '\33[97m'

