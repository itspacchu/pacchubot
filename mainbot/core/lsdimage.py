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
	
	print("adjusting black point for final output ...")
	
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
	
	print("white point selection running ...")

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
def filter(img,mode = "GCMODE",ksize = 51,whitePoint = 160,blackPoint = 60 ):


	# define values for blackPoint and whitePoint
	#blackPoint = 66
	#blackPoint = 10
	#whitePoint = 160
	#whitePoint = 250
	
	# store desired mode of operation as string
	

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
	return img

#use this command ---->
#im = cv2.imread(path)
#im = scan.filter(im,'GCMODE',51,127,61)