import cv2
import numpy as np
import hashlib
import cPickle

img = cv2.imread('img1.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT(100)
kp = sift.detect(gray,None)

key = ''
for i in kp:
    key = key + "'"+(str(i.pt)) + "',"
print(key[0:-1])

#len_key = len(key)
#teste = []
#for i in range(len_key):
#    teste.append(hashlib.md5(key[i]).hexdigest())
#print(teste)
f = open("keypoints-teste.txt", "w")
teste = key[0:-1]
f.write(teste)
print('fim')
