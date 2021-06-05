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

def find_dominant_color(imageurl:str):
    try:
        NUM_CLUSTERS = 10
        im = Image.open(requests.get(imageurl, stream=True).raw)
        im = im.resize((20, 20))      # optional, to reduce time
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        vecs, dist = scipy.cluster.vq.vq(ar, codes)        
        counts, bins = scipy.histogram(vecs, len(codes))   
        index_max = scipy.argmax(counts)                   
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        if(int(colour) > 16777215):
            return  0xff54f9
        return int(hex(int(colour, 16)), 0)
    except:
        return 0xff54f9

def __initiate_default_stats__(serverlist:dict,serverid:str):
    serverlist[serverid] = {
        'emoji':'🌊',
        'debug':0,
        'bruh':'https://media.discordapp.net/attachments/760741167876538419/760744075132534784/DeepFryer_20200930_113458.jpg?width=448&height=518',
        'prefix' : '',
        'stats': {
            'bot_summons':0,
            'ecchi_command':0,
            'hugs':0,
            'pats':0,
            'kiss':0,
            'kills':0,
            'anipics':0,
            'anime':0,
            'manga':0,
            'echos':0,
            'bruhs':0,
            'nice':0
        }
        }

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

bot_avatar_url = "https://cdn.discordapp.com/attachments/715107506187272234/850379532459573288/pacslav.png"

def __count_statistics__(serverlist:dict,serverid:str,stattitle:str):
    try:
        serverlist[serverid]['stats'][stattitle] += 1
    except KeyError:
        __initiate_default_stats__(serverlist,serverid)

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
        return queryToName(qlink)

def better_send(ctx,content=None,embed=None,file=None):
    try:
        try:
            return ctx.reply(content, embed=embed, file=file)
        except:
            return ctx.send(content, embed=embed, file=file)
    except:
        return ctx.send("Coudn't send the message.. something went wrong!!")
        

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
