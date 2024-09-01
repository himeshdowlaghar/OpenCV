import cv2
import numpy as np
framewidth=300
frameheight=300
cap=cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
mycolors=([
    [0, 100, 100, 10, 255, 255],  # Red lower range
    [170, 100, 100, 180, 255, 255],  # Red upper range
    [94, 80, 2, 126, 255, 255],  # Blue
    [20, 100, 100, 30, 255, 255]  # Yellow
])
mycolorValues=([
    [0,0,204],
    [51,51,255],
    [204,0,0],
    [0,102,204]
])
mypoints=[] ##[x,y,colorID]
def findColor(frame,mycolors,mycolorValues):
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    count=0
    newpoints=[]
    for color in mycolors:
        lower = np.array(color[0:3])  # Correct 1D array for lower bound
        upper = np.array(color[3:6])  # Correct 1D array for upper bound
        masking = cv2.inRange(imgHSV, lower, upper)
        # cv2.imshow(str(color[0]), masking)
        x,y=getcontours(masking)
        cv2.circle(imgResult,(x,y),10,mycolorValues[count],5)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count+=1
    return newpoints
def getcontours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0

    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>1000:
            # cv2.drawContours(imgResult,cnt,-1,(255,0,0),cv2.FILLED)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
            # cv2.rectangle(imgResult, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return x+w//2,y

def drawOnCanvas(mypoints,mycolorValues):
    for point in mypoints:
        cv2.circle(imgResult,(point[0],point[1]),5,mycolorValues[point[2]],cv2.FILLED)

while True:
    ret,frame=cap.read()
    imgResult=frame.copy()

    newpoints=findColor(frame,mycolors,mycolorValues)
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(mypoints)!=0:
        drawOnCanvas(mypoints,mycolorValues)
    cv2.imshow('frame',frame)
    cv2.imshow("REsult",imgResult)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break