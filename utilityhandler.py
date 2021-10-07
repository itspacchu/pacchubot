import requests
import shutil
from bs4 import BeautifulSoup
from PIL import Image
import binascii
import numpy as np

def downloadFileFromUrl(something:str,name:str):
    response = requests.get(something, stream=True)
    with open(f'{name}.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def cartoonize(myfile,filname):
    downloadFileFromUrl(myfile,filname,none=None)
    s = requests.Session()
    url = "https://cartoonize-lkqov62dia-de.a.run.app/cartoonize"
    with open(str(filname + '.png'), 'rb') as f:
        r = s.post(url, files={'image': f})  
    soup = BeautifulSoup(r.text,'html.parser')
    dlink = soup.find_all('a')[0]['href']
    downloadFileFromUrl(dlink,filname)
    s.close()
    return filname + '.png'

async def unified_imagefetcher(ctx, member=None, attachedImg=None):
    await ctx.message.add_reaction('🖼')
    try:
        if(attachedImg == None):
            attachment_url = ctx.message.attachments[0].url
        else:
            attachment_url = attachedImg
        await ctx.message.add_reaction('📩')
        return attachment_url
    except:
        try:
            hgp = member
            await ctx.message.add_reaction('🎭')
            if(ctx.message.author == hgp or hgp == None):
                attachment_url = ctx.message.author.avatar.url
            else:
                attachment_url = hgp.avatar.url
            return attachment_url
        except:
            await ctx.send("> I think something went wrong!")
            return None

def find_dominant_color(imageurl: str, local=False):
    return 0xffff00


def list_to_string(the_list, no_of_items: int):
    returnstr = ''
    count = 0
    for _ in the_list:
        if(count > no_of_items):
            break
        count += 1
        returnstr += str(_ + "\n")
    return returnstr