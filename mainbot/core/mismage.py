import cv2 as cv
import numpy as np

#lsd image functions start  here
def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def blackPointSelect(img,blackPoint):
	img = img.astype('int32')
	img = map(img, blackPoint, 255, 0, 255)
	_, img = cv.threshold(img, 0, 255, cv.THRESH_TOZERO)
	img = img.astype('uint8')
	return img

def whitePointSelect(img,whitePoint):
	_,img = cv.threshold(img, whitePoint, 255, cv.THRESH_TRUNC)

	img = img.astype('int32')
	img = map(img, 0, whitePoint, 0, 255)
	img = img.astype('uint8')
	
	return img

def highPassFilter(img,kSize=51):
	print("applying high pass filter")
	
	if not kSize%2:
		kSize +=1
		
	kernel = np.ones((kSize,kSize),np.float32)/(kSize*kSize)
	filtered = cv.filter2D(img,-1,kernel)
	filtered = img.astype('float32') - filtered.astype('float32')
	filtered = filtered + 127*np.ones(img.shape, np.uint8)
	filtered = filtered.astype('uint8')
	
	img = filtered
	return img

def highpass(imgFilename,ksize = 51,whitePoint = 127,blackPoint = 61 ):

	img = cv2.imread(imgFilename)
    if(img.shape[0] > 1024 or img.shape[1] > 1024):
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
	
	img = highPassFilter(img,ksize)
	img = whitePointSelect(img,whitePoint)
	img = blackPointSelect(img,blackPoint)
    cv2.imwrite(imgFilename, img)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	return img

#use this command ---->
#im = cv2.imread(path)
#im = scan.filter(im,'GCMODE',51,127,61)

#lsd image functions end here

#line art function starts here

def shadow(imgFilename,method = 0):

	img = cv2.imread(imgFilename)
    rgb_planes = cv2.split(img)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        #result_planes.append(diff_img) #will add methods prolly
        result_norm_planes.append(norm_img)
    #result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)
    result_norm = cv2.cvtColor(result_norm,cv2.COLOR_BGR2RGB)
    return result_norm
#lineart function ends here