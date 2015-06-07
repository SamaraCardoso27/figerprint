import cv2
import numpy as np
from skimage import morphology
import cPickle

import cv2
import numpy as np
from skimage import morphology
import cPickle



def createKeyPoints(wImage):
    img = cv2.imread(wImage)
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    sift = cv2.SIFT(500)
    kp = sift.detect(gray,None)
    img=cv2.drawKeypoints(gray,kp)
    cv2.imwrite('siftkeypoints.jpg',img)
    print('Saved Image')


def saveKeyPoints(wImage):
    im=cv2.imread(wImage)
    gr=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    d=cv2.FeatureDetector_create("SIFT")
    kp=d.detect(gr)

    index = []
    for point in kp:
        temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id) 
    index.append(temp)

    f = open("keypoints-teste.txt", "w")
    f.write(cPickle.dumps(index))
    print('Save KeyPoints')
    f.close()

def displayKeypoints():
    im=cv2.imread("sift_keypoints.jpg")
    index = cPickle.loads(open("keypoints-teste.txt").read())
    kp = []
    for point in index:
        temp = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], 
                            _response=point[3], _octave=point[4], _class_id=point[5]) 
    kp.append(temp)
    imm=cv2.drawKeypoints(im, kp);
    cv2.imwrite('display_keypoints.jpg',imm)
    print('display keypoints')
    
 
createKeyPoints('2015-05-05 21_36_36.300830.jpeg')
#createKeyPoints("dst.png")
#saveKeyPoints("sift_keypoints.jpg")
#displayKeypoints()




