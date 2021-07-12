import cv2 as cv
import numpy as np

'''
 Function to map values in range [in_min, in_max] to the range [out_min, out_max]
'''

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# global variables for image ,blackPoint, whitePoint
#img = None; whitePoint = None; blackPoint = None;


'''
* High Pass Filter
* Output of HPF depends on the kernel size provided as input argument
* Links to the docuementation:
*  Introduction: https://github.com/sourabhkhemka/DocumentScanner/wiki/Scan:-Introduction
*  HPF: https://github.com/sourabhkhemka/DocumentScanner/wiki/GCMODE
*
'''
def blackPointSelect(img,blackPoint):
	#global img
	
	
	
	# refer repository's wiki page for detailed explanation

	img = img.astype('int32')

	img = map(img, blackPoint, 255, 0, 255)

	#if cv.__version__ == '3.4.4':
	#img = img.astype('uint8')

	_, img = cv.threshold(img, 0, 255, cv.THRESH_TOZERO)

	img = img.astype('uint8')
	
	return img
	'''
	* Method to select whitePoint in the image
	*
	* Links to documentation: 
	*  Introduction: https://github.com/sourabhkhemka/DocumentScanner/wiki/Scan:-Introduction
	*  White Point Select: https://github.com/sourabhkhemka/DocumentScanner/wiki/White-Point-Select
	'''
def whitePointSelect(img,whitePoint):
	#global img
	
	

	# refer repository's wiki page for detailed explanation

	_,img = cv.threshold(img, whitePoint, 255, cv.THRESH_TRUNC)

	img = img.astype('int32')
	img = map(img, 0, whitePoint, 0, 255)
	img = img.astype('uint8')
	
	return img
	'''
	* Method to select black point in the image
	*
	* Links to documentation: 
	*  Introduction: https://github.com/sourabhkhemka/DocumentScanner/wiki/Scan:-Introduction
	*  Black Point Select: https://github.com/sourabhkhemka/DocumentScanner/wiki/Black-Point-Select
	*
	''' 

def highPassFilter(img,kSize=51):
	#global img
	
	print("applying high pass filter")
	
	if not kSize%2:
		kSize +=1
		
	kernel = np.ones((kSize,kSize),np.float32)/(kSize*kSize)
	
	filtered = cv.filter2D(img,-1,kernel)
	
	filtered = img.astype('float32') - filtered.astype('float32')
	#cv.imshow("blur sub", filtered)
	#cv.imwrite('imgart.jpg',filtered.astype('uint8'))
	#cv.waitKey(0);
	filtered = filtered + 127*np.ones(img.shape, np.uint8)
	#cv.imshow("blur sub 127", filtered)
	#cv.imwrite('imgart127.jpg',filtered.astype('uint8'))
	#cv.waitKey(0);
	filtered = filtered.astype('uint8')
	
	img = filtered
	return img
def filter(imgFilename,mode = "GCMODE",ksize = 51,whitePoint = 160,blackPoint = 60,preview = false ):


	# define values for blackPoint and whitePoint
	#blackPoint = 66
	#blackPoint = 10
	#whitePoint = 160
	#whitePoint = 250
	
	# store desired mode of operation as string
    try:
        img = cv.imread(imgFilename)
        img.shape
    except AttributeError: # to get first frame of gif
        img = cv.VideoCapture(imgFilename)
        ret, img = theim.read()

    if(img.shape[0] > 1024 or img.shape[1] > 1024):
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

	if mode == "GCMODE":
		img = highPassFilter(img,ksize)
		#whitePoint = 127
		img = whitePointSelect(img,whitePoint)
		img = blackPointSelect(img,blackPoint)
	elif mode == "RMODE":
		img = blackPointSelect(img,blackPoint)
		img = whitePointSelect(img,whitePoint)
	elif mode == "SMODE":
		img = blackPointSelect(img,blackPoint)
		img = whitePointSelect(img,whitePoint)
		img = blackAndWhite(img)

	
	
	if(preview):
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        cv2.imwrite(imgFilename, img)
	im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)



#use this command ---->
#im = cv2.imread(path)
#im = scan.filter(im,'GCMODE',51,127,61)