import numpy as np
import cv2 as cv

WIDTH = 640

# # RESCALE IMAGE
def rescale(img):
    dim = (WIDTH, int(img.shape[0] / img.shape[1] * WIDTH))
    return cv.resize(img, dim, interpolation = cv.INTER_AREA)

def nothing(args):
    pass

# # VIDEO CAPTURE LOOP
cap = cv.VideoCapture(0)

cv.namedWindow("Trackbars", flags=cv.WINDOW_FREERATIO)
cv.resizeWindow("Trackbars", 200, 600)
cv.createTrackbar("pip-thresh-lower", "Trackbars", 100, 1000, nothing)
cv.createTrackbar("pip-thresh-upper", "Trackbars", 300, 1000, nothing)
cv.createTrackbar("die-thresh-lower", "Trackbars", 1000, 10000, nothing)
cv.createTrackbar("die-thresh-upper", "Trackbars", 4000, 10000, nothing)
cv.createTrackbar("canny-thresh-lower", "Trackbars", 0, 1000, nothing)
cv.createTrackbar("canny-thresh-upper", "Trackbars", 1000, 1000, nothing)
cv.createTrackbar("epsilon%", "Trackbars", 1, 10000, nothing)
cv.createTrackbar("sigma", "Trackbars", 0, 10, nothing)
cv.createTrackbar("param1", "Trackbars", 1, 1000, nothing)
cv.createTrackbar("param2", "Trackbars", 1, 1000, nothing)

# ptu, ptl, dtu, dtl, ctu, ctl = 300, 100, 4000, 1000, 1000, 1000
while True:
    ptu = cv.getTrackbarPos("pip-thresh-upper", "Trackbars")
    ptl = cv.getTrackbarPos("pip-thresh-lower", "Trackbars")
    dtu = cv.getTrackbarPos("die-thresh-upper", "Trackbars")
    dtl = cv.getTrackbarPos("die-thresh-lower", "Trackbars")
    ctu = cv.getTrackbarPos("canny-thresh-upper", "Trackbars")
    ctl = cv.getTrackbarPos("canny-thresh-lower", "Trackbars")
    eps = cv.getTrackbarPos("epsilon%", "Trackbars")
    sig = cv.getTrackbarPos("sigma", "Trackbars")
    p1 = cv.getTrackbarPos("param1", "Trackbars") + 1
    p2 = cv.getTrackbarPos("param2", "Trackbars") + 1

    _, frame = cap.read()
    
    # SCALE, GRAY, GAUS-BLUR, CANNY-EDGE, GAUS-BLUR
    imgscaled = rescale(frame)
    imggray = cv.GaussianBlur(cv.cvtColor(imgscaled, cv.COLOR_BGR2GRAY), (5, 5), 0)
    imgedges = cv.GaussianBlur(cv.GaussianBlur(cv.Canny(imggray, ctl, ctu, apertureSize=5, L2gradient=True), (5, 5), 0), (5, 5), 0)
    

    # FIND AND SORT CONTOURS BY SIZE AND SHAPE
    dieconts = []
    pipconts = []
    for cont in cv.findContours(cv.threshold(imgedges, 25, 255, cv.THRESH_OTSU)[1], cv.RETR_TREE, cv.CHAIN_APPROX_NONE)[0]:
        cont = cv.approxPolyDP(cont, eps*cv.arcLength(cont, True)/10000, True)
        area = cv.contourArea(cont)
        if ptl < area < ptu and 10 < len(cont) < 20:
            pipconts.append(cont)
        elif dtl < area < dtu and len(cont) <= 20:
            dieconts.append(cont)

    imgedges = cv.cvtColor(imgedges, cv.COLOR_GRAY2BGR)
    cv.drawContours(imgedges, dieconts, -1, (0,255,0), 1)
    cv.drawContours(imgedges, pipconts, -1, (255,0,0), 1)

    imgcont = np.zeros((480,640,3), dtype=np.uint8)
    cv.drawContours(imgcont, pipconts, -1, (255,255,255), 1)
    imgcont = cv.GaussianBlur(cv.cvtColor(imgcont, cv.COLOR_BGR2GRAY), (3, 3), sig)

    # HOUGH CIRCLE TRANSFORM
    detected_circles = cv.HoughCircles(imgcont,  
                    cv.HOUGH_GRADIENT, 1, 20, param1 = p1, 
                param2 = p2, minRadius = 5, maxRadius = 20) 
    
    imgcirc = np.zeros((480,640,3), dtype=np.uint8)
    if detected_circles is not None: 
        detected_circles = np.uint16(np.around(detected_circles)) 
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            cv.circle(imgcirc, (a, b), r, (0, 255, 0), 2) 
            cv.circle(imgcirc, (a, b), 1, (0, 0, 255), 3) 

    # DISPLAY
    cv.imshow("contours", imgcont)
    cv.imshow("circles", imgcirc)
    cv.imshow("edges", imgedges)
    cv.imshow("Frame", imgscaled)

    key = cv.waitKey(1)
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()
