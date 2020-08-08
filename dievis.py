import numpy as np
import cv2

img_color = None
thresh = None
contours = None

def read_img(img_name):
    img = cv2.imread(img_name)
    return img

def resize(img):
    # scale_percent = 20 # percent of original size
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    width = 500
    height = int(img.shape[0]/img.shape[1] * width)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return img

def get_thresh(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 35, 255, cv2.THRESH_BINARY)
    thresh = ~thresh
    return thresh

def get_contours(thresh):
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_die_num(contourss):
    global contours
    # get rid of areas that are too small or too large
    potentials = []
    contours_cop = []
    for cont in contours:
        print("found: " + str(cv2.contourArea(cont)))
        if cv2.contourArea(cont) > 50 and cv2.contourArea(cont) < 1000:
            contours_cop.append(cont)
            potentials.append(cv2.contourArea(cont))
    # look for a cluster of 6-1 with similar areas
    contours = contours_cop
    clusters = []
    print(potentials)
    for pont in potentials:
        if len(clusters) == 0:
            clusters.append([pont])
        else:
            clust_found = False
            for i in range(len(clusters)):
                if abs(pont-clusters[i][0]) < clusters[i][0]/3:
                    clusters[i].append(pont)
                    clust_found = True
            if not clust_found:
                clusters.append([pont])
    lengths = []
    for clust in clusters:
        if len(clust) <= 6:
            lengths.append(len(clust))
    lengths.sort()
    return lengths[len(lengths)-1]

img_color = resize(read_img('img/top3.png'))
thresh = get_thresh(img_color)
contours = get_contours(thresh)
print(get_die_num(contours))

cv2.drawContours(img_color, contours, -1, (0,255,0), 3)
cv2.imshow('im', img_color)
cv2.imshow('thr', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
