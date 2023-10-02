import scipy
import scipy.misc
import scipy.cluster
from PIL import Image
import requests
import binascii

class Emotes:
    PACPILOVE = "<:pacpilove:860277910106800198>"
    PACCHU = "<:pacchu:860277741546373131>"
    PACEXCLAIM = "<:pacDoubleExclaim:858677949775872010>"
    PACSTOP = '<:pacstop:860273983614091325>'
    PACPLAY = '<:pacplay:860273984213483531>'
    PACPAUSE = '<:pacpause:860273984218464267>'
    PACDEPRESS = "<:pacdepression:860277067730649135>"
    LOFISPARKO = "<:lofisparko:858551929977962547>"
    ANGRYPING = "<:Angryping:869550989328400434>"
    PACYES = "<:pacyes:858677949812441088>"
    PACTICK = "<:pactick:858677949486333973>"
    PACCROSS = "<:paccross:858677949662363648>"
    PACNO = "<:pacno:858677949716103198>"

class Colors:
    ERR = 0xf54257
    SUCC = 0x6cf257
    NEUTRAL = 0x43ccc3
    SPOTIFY = 0x1db954
    YOUTUBE = 0xc4302b
    FALLBACK = 0xc7979
    APPLE = 0xfc3c44
    OTHER = 0xeba434

    def dominant(imageurl: str, local=False):
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
            colour = binascii.hexlify(bytearray(int(c)
                                    for c in peak)).decode('ascii')
            try:
                return int(hex(int(colour, 16))[:8], 0)
            except:
                return 0xffffff
        except IndexError:
            return 0xffffff

