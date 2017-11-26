import numpy as np
import cv2

#------------------------------------------------------------------

def cond(start, end, step):
	while start < end:
		yield start
		start   += step

#------------------------------------------------------------------

def filter_color(hsv):
	minColor = np.array([
		[0, 0, 0],								#black /
		[3, 170, 100],							#brown /
		[0, 170, 105],							#red /--- nope
		[11, 175, 160],							#orange /
		[21, 192, 157],							#yellow /
		[65, 106, 70],							#green
		[98, 136, 86],							#blue
		[144, 68, 75],							#purple
		[0, 0, 73],								#grey
		[0, 0, 200]])							#white

	maxColor = np.array([
		[180, 153, 77],							#black /
		[10, 230, 120],							#brown /
		[10, 255, 255],							#red /--- nope....
		[15, 255, 255],							#orange /
		[30, 255, 255],							#yellow /
		[60, 255, 255],							#green
		[120, 255, 255],						#blue
		[150, 255, 255],						#purple
		[8, 38, 128],							#grey
		[0, 0, 255]])							#white

	n_min = 10									#n_min = n_max

	for n in cond(0, 10, 1):
		mask = cv2.inRange(hsv, minColor[n], maxColor[n])
		cv2.imshow('mask' ,mask)
		#print n+1
		cv2.waitKey(0)
		cv2.destroyAllWindows()

#------------------------------------------------------------------

def chkSize(img):
	height, width, channels = img.shape

	if(height >= 800 or width >= 600):
		return cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
	
#------------------------------------------------------------------

def drawRect(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(5, 5), 0)
	_, bin = cv2.threshold(gray,120,255,1) # inverted threshold (light obj on dark bg)
	bin = cv2.dilate(bin, None)  # fill some holes
	bin = cv2.dilate(bin, None)
	bin = cv2.erode(bin, None)   # dilate made our shape larger, revert that
	bin = cv2.erode(bin, None)
	bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	rc = cv2.minAreaRect(contours[0])
	box = cv2.boxPoints(rc)
	for p in box:
	    	pt = (p[0],p[1])
    		print pt
    		cv2.circle(img,pt,5,(200,0,0),2)
	cv2.imshow("rect", img)
	cv2.waitKey()

#------------------------------------------------------------------

img = cv2.imread('img/R2.jpg')

img = chkSize(img)
drawRect(img)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
filter_color(hsv)

#------------------------------------------------------------------




## silver-gold -------------------------------------------------------

#lower_silver = np.array([110,50,50])
#upper_silver = np.array([130,255,255])
#mask11 = cv2.inRange(hsv, lower_silver, upper_silver)

#lower_gold = np.array([110,50,50])
#upper_gold = np.array([130,255,255])
#mask12 = cv2.inRange(hsv, lower_gold, upper_gold)

