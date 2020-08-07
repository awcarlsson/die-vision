import numpy as np
import cv2

img = cv2.imread('img/four.png')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 0, 40, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# resizing
scale_percent = 20 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
imgray = cv2.resize(imgray, dim, interpolation = cv2.INTER_AREA)

cv2.drawContours(img, contours, -1, (0,255,0), 3)

cv2.imshow('im', img)
cv2.imshow('imgrey', imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()
