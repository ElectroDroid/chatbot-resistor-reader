import numpy as np
import cv2

#------------------------------------------------------------------

def cond(start, end, step):
	while start < end:
		yield start
		start   += step

#------------------------------------------------------------------

def cond2(start, end, step):
	while start <= end:
		yield start
		start   += step

#------------------------------------------------------------------

def filter_color(img):

	x_max, x_min, y_max, y_min, img = findArea(img)
	#print x_max    #max
	#print x_min    #min
	img_tmp = img.copy();
	
	
	hsv = cv2.cvtColor(img_tmp, cv2.COLOR_BGR2HSV)
	minColor = np.array([
		[0, 0, 0],								#black /
		[0, 150, 77],							#brown /
		[0, 255, 183],							#red /
		[11, 175, 160],							#orange /
		[21, 192, 157],							#yellow /
		[43, 106, 70],							#green
		[98, 136, 86],							#blue
		[144, 68, 75],							#purple
		[0, 0, 73],								#grey
		[0, 0, 200],							#white
		[13, 124, 188]])						#gold	

	maxColor = np.array([
		[180, 153, 77],							#black /
		[10, 255, 255],							#brown /
		[0, 255, 255],							#red /
		[15, 255, 255],							#orange /
		[30, 255, 255],							#yellow /
		[60, 255, 255],							#green
		[120, 255, 255],						#blue
		[175, 255, 255],						#purple
		[8, 38, 128],							#grey
		[22, 40, 255],							#white
		[19, 186, 216]])						#gold	

	
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
		"white",
		"gold"])

	color = np.array([
		[0, 0, 0],							
		[38, 53, 71],							
		[0, 0, 255],							
		[0, 128, 255],							
		[0, 255, 255],							
		[0, 255, 0],							
		[255, 0, 0],						
		[255, 0, 200],						
		[128, 128, 128],							
		[255, 255, 255],
		[88, 158, 205]])

	colorX = []
	colorY = []
	minX = []
	maxX = []
	colorN =[]

	for n in cond(0, 10, 1):
		mask = cv2.inRange(hsv, minColor[n], maxColor[n])
		#cv2.imshow('Result' ,mask)
		#cv2.waitKey(0)

		output = cv2.bitwise_and(img_tmp, hsv, mask=mask)
		ret,thresh = cv2.threshold(mask, 40, 255, 0)
		_,contours,_ = cv2.findContours(thresh, 1, 2)

		for c in contours:
			x,y,w,h = cv2.boundingRect(c)
			
			if w < 10 or h < 35 or w > 40:
				continue

			print colorName[n]

			
			if x >= x_min and x+w < x_max and y >= y_min and y+h < y_max:
				cv2.rectangle(img,(x,y),(x+w,y+h),color[n],2)
				#cv2.imshow('Result' ,img)
				#cv2.waitKey(0)
				cX,cY = findPosition(img_tmp, c)
				colorX.append(cX)
				minX.append(x)
				maxX.append(x+w)
				colorN.append(n)
				#print colorName[n]

			
		print "-----"

	value = calculate(colorX, minX, maxX, colorN)
	ans = str(value)+" ohm"
	#ans = "ans"
	drawRect(x_max, x_min, y_max, y_min, img, ans)
	cv2.imshow('Result' ,img)	
	#cv2.putText(img,ans,(x_max+10,y_max),0,0.5,(0,0,255))
	cv2.waitKey(0)
	
	print value

#------------------------------------------------------------------

def findPosition(img, c):
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	return cX, cY

#------------------------------------------------------------------

def calculate(colorX, minX, maxX, colorN):
	#value = n;
	multiplier = np.array([
		1,								#black 
		10,								#brown 
		100,							#red 
		1000,							#orange 
		10000,							#yellow 
		100000,							#green
		1000000,						#blue
		10000000])						#purple

	str_value = ""

	order = []

	for i in cond(0,len(colorX),1):
		if i != len(colorX)-1:
			if colorN[i] == colorN[i+1] and maxX[i]-minX[i] <= 40:
				continue
		order.append([int(colorX[i]), int(colorN[i])])
		#print colorX[i]
		#print colorN[i]

	order = sorted(order, key=getKey)
	#print order
	
	str_value = order[0][1] + order[1][1]
	value = int(str_value) * multiplier[order[2][1]]
	#print order[0][1]
	return value
		
#------------------------------------------------------------------

def getKey(item):
	return item[0]

#------------------------------------------------------------------

def chkSize(img):
	height, width, channels = img.shape

	if(height > 800 or width > 600):
		return cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
	else:
		return img

#------------------------------------------------------------------

def findArea(img):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	#lower = np.array([87, 51, 170])
	#upper = np.array([103, 166, 230])
	lower = np.array([10, 64, 110]) 
	upper = np.array([20, 150, 230])  
	mask = cv2.inRange(hsv, lower, upper)
	#cv2.imshow('Result' ,mask)
	#cv2.waitKey(0)
	output = cv2.bitwise_and(img, hsv, mask=mask)

	ret,thresh = cv2.threshold(mask, 40, 255, 0)
	_,contours,_ = cv2.findContours(thresh, 1, 2)
	
	x_n = [] 
	y_n = []
	x_x = [] 
	y_x = []

	for c in contours:
			x,y,w,h = cv2.boundingRect(c)
			
			if w < 15 or h < 50:
				continue
			
			x_n.append(x)
			y_n.append(y)
			x_x.append(x+w)
			y_x.append(y+h)
			#cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

	x_max = max(x_x)
	y_max = max(y_x)
	x_min = min(x_n)
	y_min = min(y_n)
	#cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,0,255),2)
	#cv2.imshow('Result' ,img)
	#cv2.waitKey(0)

	return x_max, x_min, y_max, y_min, img

#------------------------------------------------------------------

def drawRect(x_max, x_min, y_max, y_min, img, text):
	cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,0,255),2)
	cv2.putText(img,text,(x_max+10,y_max),0,0.5,(0,0,255))

#------------------------------------------------------------------

img = cv2.imread('../img/R11.jpg')   # 5 7 10

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

