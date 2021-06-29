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


async def report_errors_to_channel(client,error):
    pass
    """print(repr(error))
    channel = await client.get_channel(501237046854287365)
    await client.send(f"```{str(repr(error))}```")"""
    


distortionTypes = [lambda i:[10*np.sin(i), 10*np.sin(i)],
                   lambda i:[10*np.sin(i), 0],
                   lambda i:[0, 10*np.sin(i)],
                   lambda i:[np.tan(i),np.cos(i)],
                   lambda i:[5*np.tan(i), 5*np.tan(i)],
                   lambda i:[5*np.tan(i), 0],
                   lambda i:[0, 5*np.tan(i)],
                   lambda i:[(i**np.sin(i)) , (i**np.sin(i))],
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
