from ctypes import *
from time import sleep
from sys import exit
import Image
import cv2
import datetime
import numpy as np

""" Create Image size  structure to pass through function"""
class FTRSCAN_IMAGE_SIZE(Structure):
	_fields_ = [('nWidth', c_int), ('nHeight', c_int), ('nImageSize', c_int)]



def PrintErrorMessage(nErrCode):
	print "Failed to obtain image. "
	if nErrCode==0:
		print "OK"
	elif nErrCode==4306:
		print "- Empty frame -"
	elif nErrCode==0x0001:
		print "- Movable finger -"
	elif nErrCode==0x0002:
		print "- Fake finger -"
	elif nErrCode==0x0004:
		print "- Incompatible hardware -"
	elif nErrCode==0x0005:
		print "- Incompatible firmware -" 
	elif nErrCode==0x0006:
		print "- Invalid authorization code -"
	else:
		print "Unknown return code - ", nErrCode

lib = cdll.LoadLibrary('/home/diego/Documents/Fingerprint/libScanAPI_Linux_Src_v12.0.1.1576/linux_x86_64bit/libScanAPI.so')

if lib == None:
	print 'Cannot open the library....'
	exit(-1) 

hDevice = lib.ftrScanOpenDevice()

if hDevice==0:
	print 'Cannot get the device, do you have permition? It is plugged?'
	exit(-1) 


ImageSize = FTRSCAN_IMAGE_SIZE(0,0,0)


if lib.ftrScanGetImageSize(hDevice,pointer(ImageSize))!=1:
	print 'Cannot get image size from device...'
	lib.ftrScanCloseDevice(hDevice)
	exit(-1) 

print 'Image Size is ',ImageSize.nImageSize


# creating a buffer for image
pBuffer = create_string_buffer(ImageSize.nImageSize)

print "Please put your finger on the scanner:\n"
while True:
	if lib.ftrScanIsFingerPresent( hDevice, None )==1:
		break;
	sleep(0.2)

print "Capturing fingerprint ......\n"
while True:
	if lib.ftrScanGetFrame(hDevice, pointer(pBuffer), None)==1:
		print "Done!\n\nWriting to file......\n"
		vect = bytearray(pBuffer.raw)
		outputIm = Image.new("RGB", (ImageSize.nWidth, ImageSize.nHeight))
		outputIm.putdata(vect)
		base_name = str(datetime.datetime.now()).replace(':','_').replace('/','_')+'.jpeg'
		outputIm.save(base_name)
		img = cv2.imread(base_name)
		gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		sift = cv2.SIFT(100)
		kp = sift.detect(gray,None)
		print kp
		img=cv2.drawKeypoints(gray,kp)
		cv2.imwrite('Processed_'+base_name,img)
		break
	else:
		PrintErrorMessage(lib.ftrScanGetLastError())
	sleep(0.2)

print 'System Terminate'
lib.ftrScanCloseDevice(hDevice)
