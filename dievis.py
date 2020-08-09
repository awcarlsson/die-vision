import numpy as np
import cv2

img_color = None
thresh = None
contours = None

def read_img(img_name):
    img = cv2.imread(img_name)
    return img

def resize(img):
    width = 500
    height = int(img.shape[0]/img.shape[1] * width)
    dim = (width, height)
    res_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return res_img

def get_thresh(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ret, thresh = cv2.threshold(imgray, 45, 255, cv2.THRESH_BINARY)
    thresh = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 45)
    thresh = ~thresh
    return thresh

def get_contours(thresh):
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_lines(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 100, 200, apertureSize = 3, L2gradient=True)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=15)
    return lines

def get_die_num(contourss):
    global contours
    # get rid of areas that are too small or too large
    potentials = []
    contours_cop = []
    for cont in contours:
        # todo: bad hardcoded nums, calculate based on image area
        if cv2.contourArea(cont) > 50 and cv2.contourArea(cont) < 1000:
            contours_cop.append(cont)
            potentials.append(cv2.contourArea(cont))
    # look for a cluster of 6-1 with similar areas
    contours = contours_cop
    clusters = []
    for pont in potentials:
        if len(clusters) == 0:
            clusters.append([pont])
        else:
            clust_found = False
            for i in range(len(clusters)):
                if abs(pont-clusters[i][0]) < clusters[i][0]/4:
                    clusters[i].append(pont)
                    clust_found = True
            if not clust_found:
                clusters.append([pont])
    lengths = []
    for clust in clusters:
        if len(clust) <= 6:
            lengths.append(len(clust))
    lengths.sort()
    if len(lengths) == 0:
        return 0
    return lengths[len(lengths)-1]

# img_color = resize(read_img('img/top3.png'))
# thresh = get_thresh(img_color)
# contours = get_contours(thresh)
# print(get_die_num(contours))

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    img_color = resize(frame)
    thresh = get_thresh(img_color)
    contours = get_contours(thresh)
    cv2.drawContours(img_color, contours, -1, (0,255,0), 3)
    #cv2.imshow("Frame", thresh)

    lines = get_lines(img_color)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(img_color,(x1,y1),(x2,y2),(0,255,0),2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    num = str(get_die_num(contours))
    cv2.putText(img_color, num, (30,330), font, 3, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("DIEVISION3000", img_color)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
