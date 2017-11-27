import numpy as np
import cv2

#------------------------------------------------------------------

def cond(start, end, step):
	while start < end:
		yield start
		start   += step

#------------------------------------------------------------------

def filter_color(img):

	x,xx,y,yy,img = drawRect(img)
	print x
	
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
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

	#n_min = 10									#n_min = n_max

	black_mask = cv2.inRange(hsv, minColor[0], maxColor[0])
	brown_mask = cv2.inRange(hsv, minColor[1], maxColor[1])
	red_mask = cv2.inRange(hsv, minColor[2], maxColor[2])
	orange_mask = cv2.inRange(hsv, minColor[3], maxColor[3])
	yellow_mask = cv2.inRange(hsv, minColor[4], maxColor[4])
	green_mask = cv2.inRange(hsv, minColor[5], maxColor[5])
	blue_mask = cv2.inRange(hsv, minColor[6], maxColor[6])
	purple_mask = cv2.inRange(hsv, minColor[7], maxColor[7])
	grey_mask = cv2.inRange(hsv, minColor[8], maxColor[8])
	white_mask = cv2.inRange(hsv, minColor[9], maxColor[9])

	roi_img = [x:(yy+y)/2, xx:((yy+y)/2)+20]

	for n in cond(0, 10, 1):
		mask = cv2.inRange(hsv, minColor[n], maxColor[n])
		#mask = cv2.bitwise_or(mask0[n], mask0[n])

		#cv2.imshow('mask' ,mask)
		#print n+1
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		
	
	#cv2.waitKey(0)

#------------------------------------------------------------------

def chkSize(img):
	height, width, channels = img.shape

	if(height >= 800 or width >= 600):
		return cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

#------------------------------------------------------------------

def drawRect(img):
	#find resistor's color >> light blue
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	#lower = np.array([87, 51, 170])
	#upper = np.array([103, 166, 230])
	lower = np.array([13, 64, 210])
	upper = np.array([18, 102, 245])
	mask = cv2.inRange(hsv, lower, upper)
	output = cv2.bitwise_and(img, hsv, mask=mask)

	ret,thresh = cv2.threshold(mask, 40, 255, 0)
	_,contours,_ = cv2.findContours(thresh, 1, 2)

	#may be got some problem with coordinate...	
	x = [] 
	y = []
	xx = [] 
	yy = []

	for c in contours:
			rect = cv2.boundingRect(c)
			
			if rect[2] < 50 or rect[3] < 50:
				continue
			#print cv2.contourArea(c)
			#print rect[2]
			x1,y1,x2,y2 = rect
			#print x2
			x.append(x1)
			y.append(y1)
			xx.append(x2+x1)
			yy.append(y2+y1)
			#x_max, y_max = getMaxCoordinate(x2+x1, y2+y1, x_max, y_max)			
			#cv2.rectangle(img,(x1,y1),(x1+x2,y1+y2),(0,0,255),2)
			
			#cv2.putText(img,'Resistor',(x1+x2+10,y1+y2),0,0.5,(0,0,255))
			
			#print x1
	#print x_max

	x_max = max(xx)
	y_max = max(yy)
	x_min = min(x)
	y_min = min(y)
	#cv2.rectangle(img,(min(x),min(y)),(x_max,y_max),(0,0,255),2)
	cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,0,255),2)
	cv2.line(img,(x_min,(y_min+y_max)/2),(x_max,(y_min+y_max)/2),(0,0,255),1)
	cv2.putText(img,'Resistor',(x_max+10,y_max),0,0.5,(0,0,255))
	# show the images
	#cv2.imshow("Result", img)
	cv2.waitKey(0)

	return x_max, x_min, y_max, y_min, img

#------------------------------------------------------------------

img = cv2.imread('../img/R2.jpg')

img = chkSize(img)

drawRect(img)

filter_color(img)

#------------------------------------------------------------------




## silver-gold -------------------------------------------------------

#lower_silver = np.array([110,50,50])
#upper_silver = np.array([130,255,255])
#mask11 = cv2.inRange(hsv, lower_silver, upper_silver)

#lower_gold = np.array([110,50,50])
#upper_gold = np.array([130,255,255])
#mask12 = cv2.inRange(hsv, lower_gold, upper_gold)

