import numpy as np
import cv2

#------------------------------------------------------------------

def cond(start, end, step):
	while start < end:
		yield start
		start   += step

#------------------------------------------------------------------

def filter_color(img):

	x_max, x_min, y_max, y_min, img = findArea(img)
	print x_max    #max
	print x_min    #min
	img_tmp = img.copy();
	drawRect(x_max, x_min, y_max, y_min, img, "Resistor")
	
	hsv = cv2.cvtColor(img_tmp, cv2.COLOR_BGR2HSV)
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

	
	colorName = np.array([
		"black",							
		"brown",							
		"red",							
		"orange",							
		"yellow",							
		"green",							
		"blue",						
		"purple",						
		"grey",							
		"white"])

	color = np.array([
		[0, 0, 0],								#black /
		[100, 170, 3],							#brown /
		[0, 0, 255],							#red /--- nope
		[160, 175, 11],							#orange /
		[157, 192, 21],							#yellow /
		[0, 0, 255],							#green
		[0, 255, 0],							#blue
		[75, 68, 144],							#purple
		[73, 0, 0],								#grey
		[255, 255, 255]])		
	

	for n in cond(0, 10, 1):
		mask = cv2.inRange(hsv, minColor[n], maxColor[n])

		output = cv2.bitwise_and(img_tmp, hsv, mask=mask)
		ret,thresh = cv2.threshold(mask, 40, 255, 0)
		_,contours,_ = cv2.findContours(thresh, 1, 2)
		print n

		for c in contours:
			x,y,w,h = cv2.boundingRect(c)
			
			if w < 15 or h < 30 or w > 40:
				continue

			print colorName[n]
			print n
			cv2.rectangle(img,(x,y),(x+w,y+h),color[n],2)
		
		print "-----"

	cv2.imshow('Result' ,img)
	cv2.waitKey(0)

#------------------------------------------------------------------

def chkSize(img):
	height, width, channels = img.shape

	if(height >= 800 or width >= 600):
		return cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

#------------------------------------------------------------------

def findArea(img):
	#find resistor's color >> light blue
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array([87, 51, 170])
	upper = np.array([103, 166, 230])
	#lower = np.array([13, 64, 210])
	#upper = np.array([18, 102, 245])
	mask = cv2.inRange(hsv, lower, upper)
	output = cv2.bitwise_and(img, hsv, mask=mask)

	ret,thresh = cv2.threshold(mask, 40, 255, 0)
	_,contours,_ = cv2.findContours(thresh, 1, 2)

	
	x_n = [] 
	y_n = []
	x_x = [] 
	y_x = []

	for c in contours:
			x,y,w,h = cv2.boundingRect(c)
			
			if w < 50 or h < 50:
				continue
			
			x_n.append(x)
			y_n.append(y)
			x_x.append(x+w)
			y_x.append(y+h)

	x_max = max(x_x)
	y_max = max(y_x)
	x_min = min(x_n)
	y_min = min(y_n)	

	return x_max, x_min, y_max, y_min, img

#------------------------------------------------------------------
def drawRect(x_max, x_min, y_max, y_min, img, text):
	cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,0,255),2)
	cv2.line(img,(x_min,(y_min+y_max)/2),(x_max,(y_min+y_max)/2),(0,0,255),1)
	cv2.putText(img,text,(x_max+10,y_max),0,0.5,(0,0,255))
#------------------------------------------------------------------

img = cv2.imread('../img/R2.jpg')

img = chkSize(img)

filter_color(img)

#------------------------------------------------------------------




## silver-gold -------------------------------------------------------

#lower_silver = np.array([110,50,50])
#upper_silver = np.array([130,255,255])
#mask11 = cv2.inRange(hsv, lower_silver, upper_silver)

#lower_gold = np.array([110,50,50])
#upper_gold = np.array([130,255,255])
#mask12 = cv2.inRange(hsv, lower_gold, upper_gold)

