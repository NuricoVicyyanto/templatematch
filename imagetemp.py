import cv2
import numpy as np
import os
from controller.controller import *

path = 'image'
orb = cv2.ORB_create(nfeatures=1000)
images = []
className = []
myList = os.listdir(path)

for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}', 0)
    images.append(imgCur)
    className.append(os.path.splitext(cl)[0])

def finDes(images):
    desList = []
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList

def finID(img, desList, thres = 15):
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList = []
    finalVal = -1
    try:
        for des in desList:
            matches = bf.knnMatch(des, des2, k = 2)
            good = []
            for m, n in matches:
                if m.distance < 0.75*n.distance:
                    good.append([m])
            matchList.append(len(good))
    except:
        pass
    if len(matchList) != 0:
        if max(matchList) > thres:
            finalVal = matchList.index(max(matchList))
    return finalVal

desList = finDes(images)

cap = cv2.VideoCapture(0)

while True:
    success, img2 = cap.read()
    imgOriginal = img2.copy()
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    id = finID(img2, desList)
    if id != -1:
        cv2.putText(imgOriginal, className[id], (50,50),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        doorAutomate(0)
    cv2.imshow('img2', imgOriginal)
    cv2.waitKey(1)