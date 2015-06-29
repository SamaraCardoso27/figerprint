import cv2
import numpy as np
from skimage import morphology
import cPickle
from matplotlib import pyplot as plt

def improveImage(wImage):
    img = cv2.imread(wImage)
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    cv2.imwrite('melhorar-imagem.jpg',gray)
    print('Saved Image')

improveImage('Processed_2015-06-27 21_19_22.512509.jpeg')


def skeletonization(wImage):
    img = cv2.imread(wImage)
    img= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    size = np.size(img)
    skel = np.zeros(img.shape,np.uint8)
     
    ret,img = cv2.threshold(img,127,255,0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
     
    while(not done):
        eroded = cv2.erode(img,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(img,temp)
        skel = cv2.bitwise_or(skel,temp)
        img = eroded.copy()
     
        zeros = size - cv2.countNonZero(img)
        if zeros==size:
            done = True
    cv2.imwrite('melhorando-skeletonization.jpg',skel)
    print('fim skeletonization')

skeletonization('melhorar-imagem.jpg')



def createKeyPoints(wImage):
    img = cv2.imread(wImage)
    sift = cv2.SIFT(20)
    kp = sift.detect(img,None)
    img=cv2.drawKeypoints(img,kp)
    cv2.imwrite('createKeyPoints.jpg',img)
    print('Saved Image-createKeyPoints')
    

createKeyPoints('melhorando-skeletonization.jpg')    


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
saveKeyPoints('createKeyPoints.jpg')


def displayKeypoints(wImage):
    im=cv2.imread(wImage)
    index = cPickle.loads(open("keypoints-teste.txt").read())
    kp = []
    for point in index:
        temp = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], 
                            _response=point[3], _octave=point[4], _class_id=point[5]) 
    kp.append(temp)
    imm=cv2.drawKeypoints(im, kp);
    cv2.imwrite('display_keypoints.jpg',imm)
    print('display keypoints')
    
 
displayKeypoints('Processed_2015-06-27 21_19_22.512509.jpeg')




def drawMatchesKNN(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatchesKNN as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated
    keypoints, as well as a list of DMatch data structure (matches)
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint
              detection algorithms
    matches - A list of matches of corresponding keypoints through a KNN
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1,:] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for (img1_idx,mat) in enumerate(matches):
        (x1,y1) = kp1[img1_idx].pt # Modified for KNN
        for mat2 in mat: # Modified for KNN
            # Get the matching keypoints for each of the images
            img2_idx = mat2.trainIdx
            # x - columns
            # y - rows
            (x2,y2) = kp2[img2_idx].pt

            # Draw a small circle at both co-ordinates
            # radius 4
            # colour blue
            # thickness = 1
            cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)
            cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

            # Draw a line in between the two points
            # thickness = 1
            # colour blue
            cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)
    # Show the image
    
    cv2.imshow('Matched Features', out)
    cv2.imwrite('comparacao.jpg',out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return out # Return the image


img1 = cv2.imread('melhorando-skeletonization.jpg',0) # queryImage
img2 = cv2.imread('melhorando-skeletonization.jpg',0) # trainImage

# Initiate SIFT detector
sift = cv2.SIFT(20)

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)

matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in xrange(len(matches))]

# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)

img3 = drawMatchesKNN(img1,kp1,img2,kp2,matches)









