import numpy as np
import cv2

#Import 
img = cv2.imread('img/four.png')

#Determine Scale
scale_percent = 10 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
#Apply Rescale
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 100, 110, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

cv2.imshow('im', img)
#cv2.imshow('imgrey', imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()
