
# Standard imports
import cv2
import numpy as np;

# Read image
im = cv2.imread("20180827_ARB2_objx4_4.jpg")

gray = cv2.copyMakeBorder(im, 5, 5, 5, 5, cv2.BORDER_CONSTANT, 255)

lower = np.array([0, 0, 0])
upper = np.array([100, 100, 100])
colormask = cv2.inRange(gray, lower, upper)

(T, thresh) = cv2.threshold(colormask, 1, 255, cv2.THRESH_BINARY)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 175
params.maxArea = 10000

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.0

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.90

# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.0

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(thresh)

# Remove keypoint if on a colored bead
NewKP = []
for keypoint in keypoints:
    x = int(keypoint.pt[0])
    y = int(keypoint.pt[1])
    BGRValue = im[y - 1, x - 1]
    if BGRValue[2] >= 50 and BGRValue[1] >= 50 and BGRValue[0] >= 50:
        NewKP.append([y,x])
# Draw detected blobs as red circles.

for i in range(len(NewKP)):
    cv2.circle(im, (NewKP[i][1], NewKP[i][0]), 30, (0,0,255), 5)
# Show blobs
cv2.imshow("Keypoints", im)
cv2.waitKey(0)
