import cv2
import numpy as np
import os
#from controller.controller import *
import winsound

path = 'image'
orb = cv2.ORB_create(nfeatures=1000)
images = []
className = []
myList = os.listdir(path)
font = cv2.FONT_HERSHEY_DUPLEX
org = (30, 30)
font_color = (255, 255, 255)
thickness = 2
font_scale = 1

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
        cv2.putText(imgOriginal, className[id], org, font, font_scale, font_color, thickness, cv2.LINE_AA)
        #doorAutomate(0)
        if className[id] == "Batik Megamendung":
            winsound.PlaySound('sound/batikMegamendung.wav', winsound.SND_FILENAME)
        elif className[id] == "Batik Kawung":
            winsound.PlaySound('sound/batikKawung.wav', winsound.SND_FILENAME)
    cv2.imshow('App', imgOriginal)
    cv2.waitKey(1)