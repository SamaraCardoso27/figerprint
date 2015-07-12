import cv2
import numpy as np
from skimage import morphology
import cPickle
from matplotlib import pyplot as plt
import hashlib

def improveImage(wImage):
    img = cv2.imread(wImage)
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    cv2.imwrite('improveImage-1.jpg',gray)
    print 'gray'
    return gray


def skeletonization(wGray):
    image = wGray
    size = np.size(image)
    skeletonization_img = np.zeros(image.shape,np.uint8)
     
    ret,image = cv2.threshold(image,127,255,0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
     
    while(not done):
        eroded = cv2.erode(image,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(image,temp)
        skeletonization_img = cv2.bitwise_or(skeletonization_img,temp)
        image = eroded.copy()
     
        zeros = size - cv2.countNonZero(image)
        if zeros==size:
            done = True
    cv2.imwrite('skeletonization-1.jpg',skeletonization_img)
    print('fim skeletonization-1')
    return skeletonization_img
    

def createKeyPoints(wImage):
    sift = cv2.SIFT(20)
    kp = sift.detect(wImage,None)
    keyPoints=cv2.drawKeypoints(wImage,kp)
    cv2.imwrite('createKeyPoints-1.jpg',keyPoints)
    print('Saved Image-createKeyPoints-1')
    return keyPoints
    
def saveKeyPoints(keyPoints):
    d=cv2.FeatureDetector_create("SIFT")
    kp=d.detect(keyPoints)

    index = []
    for point in kp:
        temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id) 
    index.append(temp)

    f = open("keypoints-teste-1.txt", "w")
    f.write(cPickle.dumps(hashlib.md5(''.join(str(e) for e in index)).hexdigest()))
    print('Save KeyPoints')
    f.close()
  

