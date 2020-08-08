import cv2 as cv
import numpy as np

# # IMPORT IMAGE
img = cv.imread('img/four.png')

# # RESCALE IMAGE
SCALE_PERCENT = 30 # percent of original size
width = int(img.shape[1] * SCALE_PERCENT / 100)
height = int(img.shape[0] * SCALE_PERCENT / 100)
dim = (width, height)
img = cv.resize(img, dim, interpolation = cv.INTER_AREA)
img = cv.GaussianBlur(img, (5, 5), 0)

# # GRAYSCALE
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# gray = cv.GaussianBlur(gray, (3, 3), 0)
# cv.imshow('gray', gray)

# # CANNY EDGE-DETECTION
edges = cv.Canny(gray, 0, 150, apertureSize = 3, L2gradient=True)
# edges = cv.GaussianBlur(edges, (3, 3), 0)
# cv.imshow('edges', edges)

# # PROBABILISTIC HOUGH TRANSFORM LINE-DETECTION
lines = cv.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=15)
if lines is not None:
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    cv.imshow('houghlines3', img)

# # # HOUGH TRANSFORM LINE-DETECTION
# lines = cv.HoughLines(edges, 1, np.pi/180, 200)
# if lines is not None:
#     for line in lines:
#         rho, theta = line[0]
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a*rho
#         y0 = b*rho
#         x1 = int(x0 + 1000*(-b))
#         y1 = int(y0 + 1000*(a))
#         x2 = int(x0 - 1000*(-b))
#         y2 = int(y0 - 1000*(a))
#         cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)
#     cv.imshow('houghlines3', img)

# # LAPLACIAN
log = cv.Laplacian(gray, cv.CV_64F, ksize=5)
# cv.imshow('lapl of gauss', log)

# # EXIT
cv.waitKey(0)
cv.destroyAllWindows()