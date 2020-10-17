from random import choice
from numpy import load as nl

def joyreactor():
    f = open("joyreactor(REDONE).bin.npy","rb")
    aa = nl(f,allow_pickle = True)
    aaa=choice(aa)
    return aaa



def imgbin():
    f = open("imgbin.bin.npy","rb")
    aa = nl(f,allow_pickle = True)
    aaa=choice(aa)
    return aaa


def img2wall():
    f = open("links2wall.bin.npy","rb")
    aa = nl(f,allow_pickle = True)
    aaa=choice(aa)
    return aaa


def src3():
    f = open("src3.bin.npy","rb")
    aa = nl(f,allow_pickle = True)
    aaa=choice(aa)
    return aaa