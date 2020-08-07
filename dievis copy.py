import numpy as np
import cv2
from matplotlib import pyplot as plt

#Import 
img = cv2.imread('img/four.png')

#Determine Scale
scale_percent = 20 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
#Apply Rescale
im = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

#Grayscale Threshold and Contour
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# imgray = cv2.cvtColor(imgray, cv2.COLOR_GRAY2BGR)
# imhsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
# #ret, thresh = cv2.threshold(imgray, 10, 255, cv2.THRESH_BINARY)
# #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# #cv2.drawContours(img, contours, -1, (0, 255, 0), 3)


# # define range of blue color in HSV
# lower_die_color = np.array([0, 0, 0])
# upper_die_color = np.array([255, 80, 140])

# # Threshold the HSV image to get only blue colors
# mask = cv2.inRange(imhsv, lower_die_color, upper_die_color)

# # Bitwise-AND mask and original image
# res = cv2.bitwise_and(im, im, mask= mask)

edges = cv2.Canny(im,100,200)
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()

cv2.imshow('masked', res)
#cv2.imshow('imHSV', imhsv)
#cv2.imshow('imcol', imcol)
cv2.imshow('im', im)
#cv2.imshow('imgrey', imgray)
#cv2.imshow('thr', thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()