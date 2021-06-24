"""
Basically stuff which requires web parsing and stuff go here
"""

import numpy as np
from PIL import Image,ImageSequence
from io import FileIO
from numpy.lib.twodim_base import triu_indices_from
import requests,shutil
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from libgen_api import LibgenSearch

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
    #return filname


def downloadFileFromUrl(something:str,name:str):
    response = requests.get(something, stream=True)
    with open(f'{name}.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def FetchBookFromLibgenAPI(searchQuery:str,bAuthor=None):
    x = LibgenSearch().search_title(searchQuery)
    if(bAuthor == None):
        return x[0]
    else:
        sanity_counter = 0
        print(f"{searchQuery} by {bAuthor}")
        for book in tqdm(x):
            sanity_counter += 1
            
            print(book['Title'],' \n-----\n' ,book['Author'])
            print(bAuthor)
            if(bAuthor.lower().replace(' ','') in str(book['Author']).replace(' ','').lower()):
                return book
            if(sanity_counter > 5):
                return None


#very shitty implementation i know but well 512,512 is a small image
def distortImage(theImage,fxn,ctx=None,discordToken=None):
    info = None
    is_gif = False
    if(theImage.is_animated):
        is_gif = True
        theImage = ImageSequence.Iterator(theImage)[0].copy()
        newImg = Image.new('RGBA',theImage.size,(255,255,255))
        newImg.paste(theImage,(0,0),0)
        theImage = newImg
    imRatio = theImage.size[0]/theImage.size[1]
    if(theImage.size[0] > 512 or theImage.size[1] > 512):
        theImage = theImage.resize((512,int(512/imRatio)))
        info = "Image has been Downsampled to 512p (Low on CPU budget ;--;)"
    
    if(is_gif):
        bc,gc,rc,_ = theImage.split()
        bc = np.asarr
    else:
        theImage = np.asarray(theImage)
        bc,gc,rc = theImage[:,:,0] , theImage[:,:,1] ,theImage[:,:,2]
    dc = []
    for imgChannel in bc,gc,rc: 
        dImg = np.zeros(imgChannel.shape)
        Image.fromarray(dImg)
        for i in tqdm(range(theImage.shape[0])):
            for j in range(theImage.shape[1]):
                try:
                    dImg[i][j] = imgChannel[i + int(fxn(i)[0])][j + int(fxn(j)[1])]
                except IndexError:
                    dImg[i][j] = imgChannel[i][j]
        dc.append(dImg)   
    imr = Image.fromarray(dc[0]).convert('L')
    img = Image.fromarray(dc[1]).convert('L')
    imb = Image.fromarray(dc[2]).convert('L')
    merged=Image.merge("RGB",(imr,img,imb))
    return merged,info


async def instance_convolve(mainim, kernel):
    kx, ky = kernel.shape
    ix, iy = mainim.shape
    ox, oy = int(np.floor(kx/2)), int(np.floor(ky/2))
    conv_arr = np.zeros((ix, iy))
    for mi in range(ix):
        for mj in range(iy):
            for i in range(kx):
                for j in range(ky):
                    try:
                        conv_arr[mi][mj] += kernel[i-ox][j-ox] * \
                            mainim[i+mi][j+mj]
                    except IndexError:
                        conv_arr[mi][mj] += 0  # borders are zeros
    return conv_arr


async def normal_2D(x, y, varience=1):
    expr = 1/(2*np.pi*varience**2)*np.exp(-1*(x**2 + y**2)/2*varience**2)
    return expr


async def gaussian_kernel(sx, sy, var):
    testker = np.zeros((sx, sy))
    mulmag = 1/(2*np.pi*var**2)
    for i in range(sx):
        for j in range(sy):
            testker[i][j] = mulmag*normal_2D(i-sx/2, j-sy/2, var)

"""kx = testim.shape[0]
fftim = np.fft.fftshift(np.fft.fft2(testim))


kernelmult = fftim * testker
ifftim = np.fft.ifft2(kernelmult)
Image.fromarray(np.abs(ifftim)).show()
"""
