# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#--------------------------------------------------------
#importing communication with arduino
import smbus
import time

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number
#--------------------------------------------------------

#me added for numpy 
import numpy as np


def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray
     
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.3)

 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
    
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	cv2.imshow("Gray", gray)
	
	
	# to print the blue rectangle we need to convert it to rgb again
	backtorgb = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
	
	# draw the rectangle
	cv2.rectangle(backtorgb, ( 40,220), ( 600,260 ), (0,255,0), 2)
	
		
	# show the frame
	# cv2.imshow("Frame", backtorgb)
	# key = cv2.waitKey(1) & 0xFF
 
        # take ROI
	# CAREFUL ABOUT NEW SIZES
	
	roi = gray[220:260,40:600]
	
        #print roi.shape  
    
    
	# show the frame
	#cv2.imshow("Region of interest", roi)
	#key = cv2.waitKey(1) & 0xFF
	
	# filter 
	blur = cv2.GaussianBlur(roi,(7,7),0)
	        
	# Do threshold
 	
	retval, threshold   = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

	# show the frame
	#cv2.imshow("Frame2", threshold)
	#key = cv2.waitKey(1) & 0xFF
		
	dilated = cv2.dilate(threshold, np.ones((7, 7)))
	eroded  = cv2.erode(dilated, np.ones((7, 7)))

	# show the frame
	#cv2.imshow("Eroded", eroded)
	#key = cv2.waitKey(1) & 0xFF
	
	sum_x =  np.sum (eroded,axis = 0)
	
	left_max = np.argmax(sum_x)	
	right_max = 560 - np.argmax(np.flipud(sum_x))
	mid_line = (left_max + right_max)/2
	#right_max = 560 - np.argmax(sum_x[::-1])	

	error = 280 - mid_line	
	error_arduino = int((mid_line*5)/14)
	
	print left_max,right_max, error, error_arduino;
	
	writeNumber(error_arduino)
	
        print "RPI: Hi Arduino, I sent you ", error_arduino
        # sleep one second       
        time.sleep(0.1)
        number = readNumber()
	
	
        print "Arduino: Hey RPI, I received a digit ", number
    	
	#retval, threshold = cv2.threshold(roi, 100, 1, cv2.THRESH_BINARY_INV)
	
	#threshold = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 127, 1)

	# show the frame
	#cv2.imshow("Frame", threshold)
	#key = cv2.waitKey(1) & 0xFF
	
	#print np.sum (thresholda,axis = 0)
	
	wide = cv2.Canny(eroded, 10, 210)
	# show the frame
	#cv2.imshow("Frame", wide)
	#key = cv2.waitKey(1) & 0xFF
	
	
		
	backtorgb = cv2.cvtColor(wide,cv2.COLOR_GRAY2RGB)
	cv2.rectangle(backtorgb, ( 240,0), ( 320,40), (0,255,0), 2)
	cv2.line(backtorgb, ( 280,0), ( 280,40), (0,255,255), 2)
	cv2.line(backtorgb, ( right_max,0), ( right_max,40), (255,255,0), 2)
	cv2.line(backtorgb, ( left_max,0), ( left_max,40), (255,255,0), 2)
	cv2.line(backtorgb, ( mid_line,0), ( mid_line,40), (0,255,0), 2)
	
	# show the frame
	cv2.imshow("BacktoRGB", backtorgb)
	key = cv2.waitKey(1) & 0xFF
	

 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
           break
