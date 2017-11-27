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
		#cv2.imshow('mask' ,mask)
		#print n+1
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()

#------------------------------------------------------------------

def chkSize(img):
	height, width, channels = img.shape

	if(height >= 800 or width >= 600):
		return cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
	
#------------------------------------------------------------------


def getMaxCoordinate(x, y, x_max, y_max):
	if x > x_max and y > y_max:
		x_max = x
		y_max = y

	return x_max, y_max
	
#------------------------------------------------------------------

def drawRect(img):
	#find resistor's color >> light blue
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array([90, 51, 217])
	upper = np.array([103, 102, 230])
	mask = cv2.inRange(hsv, lower, upper)
	#output = cv2.bitwise_and(img, hsv, mask=mask)

	ret,thresh = cv2.threshold(mask, 40, 255, 0)
	_,contours,_ = cv2.findContours(thresh, 1, 2)

	#may be got some problem with coordinate...
	x_max = 0
	y_max = 0 
	x = [] 
	y = []

	for c in contours:
			rect = cv2.boundingRect(c)
			if rect[2] < 100 or rect[3] < 100:
				continue
			print cv2.contourArea(c)
			x1,y1,x2,y2 = rect
			x.append(x1)
			y.append(y1)
			x_max, y_max = getMaxCoordinate(x2+x1, y2+y1, x_max, y_max)			
			
			
			print x1
	print x_max

	cv2.rectangle(img,(x[1],y[1]),(x_max,y_max),(0,0,255),2)
	cv2.line(img,(x[1],(y[1]+y_max)/2),(x_max,(y[1]+y_max)/2),(0,0,255),1)
	cv2.putText(img,'Resistor',(x[1]+10,y_max),0,0.5,(0,0,255))
	# show the images
	cv2.imshow("Result", img)
	cv2.waitKey(0)

#------------------------------------------------------------------

img = cv2.imread('../img/R2.jpg')

img = chkSize(img)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
drawRect(img)
filter_color(hsv)

#------------------------------------------------------------------




## silver-gold -------------------------------------------------------

#lower_silver = np.array([110,50,50])
#upper_silver = np.array([130,255,255])
#mask11 = cv2.inRange(hsv, lower_silver, upper_silver)

#lower_gold = np.array([110,50,50])
#upper_gold = np.array([130,255,255])
#mask12 = cv2.inRange(hsv, lower_gold, upper_gold)

