import numpy as np
import cv2

img_color = None
thresh = None
contours = None

def read_img(img_name):
    img = cv2.imread(img_name)
    return img

def resize(img):
    scale_percent = 20 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return img
    #th2 = cv2.resize(imgray, dim, interpolation = cv2.INTER_AREA)
    #thresh = cv2.resize(thresh, dim, interpolation = cv2.INTER_AREA)
    #cv2.drawContours(imgray, contours, -1, (0,255,0), 3)

def get_thresh(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 35, 255, cv2.THRESH_BINARY)
    thresh = ~thresh
    return thresh

def get_contours(thresh):
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours:
        print(cv2.contourArea(cont))
    return contours

img_color = resize(read_img('img/top.png'))
thresh = get_thresh(img_color)
contours = get_contours(thresh)

cv2.drawContours(img_color, contours, -1, (0,255,0), 3)
cv2.imshow('im', img_color)
cv2.imshow('thr', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
