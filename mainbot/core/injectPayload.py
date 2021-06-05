import numpy as np
from PIL import Image
from io import FileIO
import requests,shutil
from bs4 import BeautifulSoup
import time

def cartoonize(myfile,filname,none=None):
    downloadFileFromUrl(myfile,filname)
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


#very shitty implementation i know but well 512,512 is a small image


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
