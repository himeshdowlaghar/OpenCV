import cv2
import numpy as np

# Set frame width and height for the camera
framewidth = 300
frameheight = 300

# Start video capture from the webcam
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)

# Define the color ranges in HSV for detection and their corresponding BGR values for drawing
mycolors = [
    [0, 100, 100, 10, 255, 255],  # Red lower range
    [170, 100, 100, 180, 255, 255],  # Red upper range
    [94, 80, 2, 126, 255, 255],  # Blue
    [20, 100, 100, 30, 255, 255]  # Yellow
]

mycolorValues = [
    [0, 0, 204],   # Red
    [51, 51, 255], # Blue
    [204, 0, 0],   # Dark Blue
    [0, 102, 204]  # Yellow
]

# This will store the points to be drawn on the canvas
mypoints = []  # [x, y, colorID]

def findColor(frame, mycolors, mycolorValues):
    """Finds the colors in the frame and returns the points to draw."""
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    count = 0
    newpoints = []
    for color in mycolors:
        lower = np.array(color[0:3])  # Lower bound for color
        upper = np.array(color[3:6])  # Upper bound for color
        masking = cv2.inRange(imgHSV, lower, upper)
        x, y = getcontours(masking)
        if x != 0 and y != 0:
            newpoints.append([x, y, count])
        count += 1
    return newpoints

def getcontours(img):
    """Detects contours in the given image and returns the center coordinates of the largest contour."""
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y

def drawOnCanvas(mypoints, mycolorValues):
    """Draws circles on the canvas at the specified points."""
    for point in mypoints:
        cv2.circle(imgResult, (point[0], point[1]), 5, mycolorValues[point[2]], cv2.FILLED)

while True:
    ret, frame = cap.read()
    imgResult = frame.copy()

    # Find and store new points to draw
    newpoints = findColor(frame, mycolors, mycolorValues)
    if newpoints:
        mypoints.extend(newpoints)
    
    # Draw on the canvas using the stored points
    if mypoints:
        drawOnCanvas(mypoints, mycolorValues)

    # Display the result
    cv2.imshow("Result", imgResult)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
