'''
MIT License

Copyright (c) 2018 LiamZ96

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
#Requirements in this file: 3.1.7, 3.1.8, 3.1.9, 3.1.10, 3.2.4, 3.2.5, 3.3.1
#Authors: Jacob Wakefield, McKenna Gates

import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
import random
import math
import itertools
import csv
import sys
from enum import Enum
from os import listdir, path
from . import util
from . import color_labeler

"""
    Description: an enum class to handle the HoughCircle configuration values that are used in cv2.HoughCircles().
"""
class HoughConfig(Enum):

    # 4x magnification
    OBJX4 = { "dp": 1,"minDist": 40,"param1": 50,"param2": 55,"minRadius": 0,"maxRadius": 75 }

    # 10x magnification
    OBJX10 = { "dp": 1,"minDist": 60,"param1": 65,"param2": 68,"minRadius": 0,"maxRadius": 125 }

"""
    Description: a class to deal with counting microbeads in a stitched image.
"""
class Counting:

    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.grayScaleMap = cv2.imread(imagePath,0) # create grayscale cv2 img
        self.colorMap = cv2.imread(imagePath) # create color cv2 img
        self.colorBeads = []
        self.crushedBeads = []
        self.waterBeads = []
    """
        Description: a function that takes a map of images and counts the beads.
        @Param houghConfig - a HoughConfig object that contains the values for the HoughCircles() function
        @return an object containing information collected during the counting process.
    """
    def getColorBeads(self, houghConfig, detectionParams):
        houghConfig = houghConfig.value
        result = []

        img = self.grayScaleMap
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        blur = cv2.GaussianBlur(img,(7,7),0)
        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,dp=houghConfig["dp"],minDist=houghConfig["minDist"],
                            param1=houghConfig["param1"],param2=houghConfig["param2"],minRadius=houghConfig["minRadius"],maxRadius=houghConfig["maxRadius"])

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # i[0] is x coordinate, i[1] is y coordinate, i[2] is radius
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


            if detectionParams.detectionAlgorithm == "avg":
                color = self.getAverageColor(i)
            elif detectionParams.detectionAlgorithm == "mid":
                color = self.getMiddleColor(i)
            elif detectionParams.detectionAlgorithm == "corner":
                color = self.getFourQuadrantColor(i)
            elif detectionParams.detectionAlgorithm == "rad":
                color = self.getRadiusAverageColor(i)


            if(color[1] == 'bead'): # if the bead is a water bead, leave it out.
                self.colorBeads.append(color)
                result.append(color)
            
        #Get the water bubble array that contains the xy coordinates and the size.
        if detectionParams.wantsWaterBubbles: 
            self.GetWaterBubbles()

        if detectionParams.wantsCrushedBeads: # if the user wants to detect crushed beads.
            self.getCrushedBeads(cimg, circles)

        imagePath = '/'.join(self.imagePath.split('/')[:-2]) + '/results/'
        imagePath += 'result_image.jpg'#+ str(fileNum) +'.jpg'
        cv2.imwrite(imagePath, cimg)

        return result

    """
        Description: a function that takes an image and finds the water bubbles in it
        @return an array with x,y coordinates for the center of each water bubble and the size of the water bubble
    """
    def GetWaterBubbles(self):
        # Read image
        im = self.colorMap
        #Create a white border around the image to detect partial water bubbles
        bordered = cv2.copyMakeBorder(im, 5, 5, 5, 5, cv2.BORDER_CONSTANT, 255)
        #Create a version of the image that makes values greater than a certain RGB value black, and those below white, then inverst it for blob detection
        lower = np.array([0, 0, 0])
        upper = np.array([120, 120, 120])
        colormask = cv2.inRange(bordered, lower, upper)
        (T, thresh) = cv2.threshold(colormask, 1, 255, cv2.THRESH_BINARY)

        # Setup SimpleBlobDetector parameters
        params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        params.minThreshold = 10
        params.maxThreshold = 200
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 16
        params.maxArea = 10000
        # Filter by Circularity
        params.filterByCircularity = False
        params.minCircularity = .0
        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.90
        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.0

        # Create a detector with the parameters
        detector = cv2.SimpleBlobDetector_create(params)
        # Detect blobs.
        keypoints = detector.detect(thresh)

        # Remove keypoint if on a colored bead, and adds the size of the bubble to the array.
        NewKP = []
        for keypoint in keypoints:
            y = int(keypoint.pt[0])
            x = int(keypoint.pt[1])
            radius = np.sqrt(keypoint.size / 3.1415)
            if radius < 1:
                radius = 1
            BGRValue = im[x, y]
            if BGRValue[2] >= 50 and BGRValue[1] >= 50 and BGRValue[0] >= 50:
                self.waterBeads.append([[0, 0, 0], 'waterBead', [y, x, radius]])
        

    def getCrushedBeads(self, image, circles):
        temp_img = self.grayScaleMap.copy()

        for i in circles[0,:]:
            # fills in the circle
            cv2.circle(temp_img, (i[0],i[1]) ,i[2], (255,255,255), -1)
            #fills the outer edges of the circle
            cv2.circle(temp_img,(i[0], i[1]), i[2], (255,255,255), 17)


        blur = cv2.GaussianBlur(temp_img, (19, 19), 0)
        lab = cv2.cvtColor(self.colorMap, cv2.COLOR_BGR2LAB)
        thresh = cv2.threshold(blur, 225, 255, cv2.THRESH_BINARY_INV)[1]
        img_output, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cl = color_labeler.ColorLabeler()

        for c in contours:
            color = cl.label(lab, c)

            if color not in cl.colorsToIgnore:
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

                # compute the center of the contour
                M = cv2.moments(c)
                if M['m00'] > 0:
                    cX = int((M["m10"] / M["m00"]))
                    cY = int((M["m01"] / M["m00"]))
                    self.crushedBeads.append([[0, 0, 0], 'crushedBead', [cX, cY, 35]])
                else:
                    cX = 0
                    cY = 0
                cv2.circle(image, (cX, cY), 2, (0, 255, 0), 3)

    #Description: a function that takes a cicle's RGB values and returns if it is water or not
    #@param RGB - tuple containing the average red, green, and blue values of a circle
    #@return a boolean that will be True if the circle is water           
    def isWater(self, RGB):
        red = RGB[0]
        green = RGB[1]
        blue = RGB[2]
        isWater = False


        maxRGBValue = 230
        minRGBValue = 3

        if red >= maxRGBValue and green >= maxRGBValue and blue >= maxRGBValue:
            isWater = True
        if red <= minRGBValue and green <= minRGBValue and blue <= minRGBValue:
            isWater = True
        return isWater


    """
        Description: a function that takes an array representing a circle's[x-coord of center, y-coord of center, radius]
                    and returns a list containing tuple with the bead's average RGB values of the top 10% and boolean isWater
        @param circleInfo - array that contains a circle's x and y coordinates of the center and the radius of the circle
        @param imageMap - a map (image) of the microscope images in color.
        @return a list containing tuple with average RGB values of top 10% from bead, boolean isWater, and x,y,radius value of the bead.
    """
    def getBrightestColor(self, circleInfo):
        img = self.colorMap
        imgY = img.shape[0]
        imgX = img.shape[1]
        x = circleInfo[0]
        y = circleInfo[1]
        radius = circleInfo[2]
        reds, greens, blues = [], [], []

        points = self.getPointsInCircle(radius, x, y)
        colorsList = []
        coordinates = list(points)

        for xCoord, yCoord in coordinates:
            if (xCoord >= imgX) or (yCoord >= imgY):
                pass
            else:
                bgrValue = img[yCoord, xCoord]
                RGB = ( bgrValue[2], bgrValue[1], bgrValue[0] )
                colorsList.append(RGB)

        sortedByRed = sorted(colorsList, key=lambda tup: tup[0], reverse=True)
        sortedByGreen = sorted(colorsList, key=lambda tup: tup[1], reverse=True)
        sortedByBlue = sorted(colorsList, key=lambda tup: tup[2], reverse=True)

        # may need to be adjusted
        tenPercent = math.floor(0.10 * len(colorsList))

        for i in range(0, tenPercent):
            reds.append(sortedByRed[i][0])
            greens.append(sortedByGreen[i][1])
            blues.append(sortedByBlue[i][2])

        average = (round(np.mean(reds), 2), round(np.mean(greens), 2), round(np.mean(blues), 2))
        isWater = self.isWater(average)
        type = 'waterBead' if isWater else 'bead'
        return [[average[0],average[1],average[2]], type, [circleInfo[0],circleInfo[1],circleInfo[2]]] #[[R,G,B], isWater, [x,y,radius]]


    def getAverageColor(self, circleInfo):
        img = self.colorMap
        imgY = img.shape[0]
        imgX = img.shape[1]
        x = circleInfo[0]
        y = circleInfo[1]
        radius = circleInfo[2]
        reds, greens, blues = [], [], []

        points = self.getPointsInCircle(radius, x, y)
        coordinates = list(points)

        for xCoord, yCoord in coordinates:
            if (xCoord >= imgX) or (yCoord >= imgY):
                pass
            else:
                bgrValue = img[yCoord, xCoord]
                reds.append(bgrValue[2])
                greens.append(bgrValue[1])
                blues.append(bgrValue[0])

        average = (round(np.mean(reds), 2), round(np.mean(greens), 2), round(np.mean(blues), 2))
        isWater = self.isWater(average)
        type = 'waterBead' if isWater else 'bead'
        return [[average[0],average[1],average[2]], type, [circleInfo[0],circleInfo[1],circleInfo[2]]] #[[R,G,B], isWater, [x,y,radius]]

    def getMiddleColor(self, circleInfo):
        img = self.colorMap
        imgY = img.shape[0]
        imgX = img.shape[1]
        x = circleInfo[0]
        y = circleInfo[1]
        radius = circleInfo[2]
        reds, greens, blues = [], [], []

        points = self.getPointsInCircle(radius/4, x, y)
        coordinates = list(points)

        for xCoord, yCoord in coordinates:
            if (xCoord >= imgX) or (yCoord >= imgY):
                pass
            else:
                bgrValue = img[yCoord, xCoord]
                reds.append(bgrValue[2])
                greens.append(bgrValue[1])
                blues.append(bgrValue[0])

        average = (round(np.mean(reds), 2), round(np.mean(greens), 2), round(np.mean(blues), 2))
        isWater = self.isWater(average)
        type = 'waterBead' if isWater else 'bead'
        return [[average[0],average[1],average[2]], type, [circleInfo[0],circleInfo[1],circleInfo[2]]] #[[R,G,B], isWater, [x,y,radius]]


    def getRadiusAverageColor(self, circleInfo):
        img = self.colorMap
        imgY = img.shape[0]
        imgX = img.shape[1]
        x = circleInfo[0]
        y = circleInfo[1]
        radius = circleInfo[2]
        reds, greens, blues = [], [], []

        for xCoord in range(x - radius + 5, x + radius - 5):
            if(xCoord >= imgX):
                pass
            else:
                bgrValue = img[y, xCoord]
                reds.append(bgrValue[2])
                greens.append(bgrValue[1])
                blues.append(bgrValue[0])

        average = (round(np.mean(reds), 2), round(np.mean(greens), 2), round(np.mean(blues), 2))
        isWater = self.isWater(average)
        type = 'waterBead' if isWater else 'bead'
        return [[average[0],average[1],average[2]], type, [circleInfo[0],circleInfo[1],circleInfo[2]]] #[[R,G,B], isWater, [x,y,radius]]


    def getFourQuadrantColor(self, circleInfo):
        img = self.colorMap
        imgY = img.shape[0]
        imgX = img.shape[1]
        x = circleInfo[0]
        y = circleInfo[1]
        radius = circleInfo[2]
        reds, greens, blues = [], [], []

        for i in range(0, 4):
            currentPoints = self.getPointsInCircle(radius/10, x + math.ceil((radius/2) * math.cos(math.radians(90*i + 45))), y + math.ceil((radius/2) * math.sin(math.radians(90*i + 45))))
            currentCoordinates = list(currentPoints)

            for xCoord, yCoord in currentCoordinates:
                if (xCoord >= imgX) or (yCoord >= imgY):
                    pass
                else:
                    bgrValue = img[yCoord, xCoord]
                    reds.append(bgrValue[2])
                    greens.append(bgrValue[1])
                    blues.append(bgrValue[0])

        average = (round(np.mean(reds), 2), round(np.mean(greens), 2), round(np.mean(blues), 2))
        isWater = self.isWater(average)
        type = 'waterBead' if isWater else 'bead'
        return [[average[0],average[1],average[2]], type, [circleInfo[0],circleInfo[1],circleInfo[2]]] #[[R,G,B], isWater, [x,y,radius]]

    """
        Description: a function that takes a bead's radius and x and y coordinates of the center and returns coordinates of every point in
                    the bead
        @param radius - radius of bead
        @param centerX - X coordinate of the center of bead
        @param centerY - Y coordinate of the center of bead
        @return a zip of the coordinates within a circle
    """
    def getPointsInCircle(self, radius, centerX, centerY):
        a = np.arange(radius + 1)
        for x, y in zip(*np.where(a[:, np.newaxis]**2 + a**2 <= radius**2)):
            # x and y given here were assuming that the center was at 0,0 therefore you must add the actual center coordinates to give accurate ones back
            yield from set((( centerX + x, centerY + y), (centerX + x, centerY -y), (centerX -x, centerY + y), (centerX -x, centerY -y),))


    """
        Description:
        @param colorFormat: a string that is either 'rgb', 'hsv', 'cmyk', or 'grayscale'
        @return void, writes file directly from class attributes
    """
    def makeBeadsCSV(self, colorFormat):
        newPath = self.imagePath
        endIndex = newPath.rfind("/")
        newPath = newPath[:endIndex]
        newPath = newPath.replace("maps", "results")
        newPath = newPath + "/beads.csv"

        util.makeBeadsCSV(newPath, colorFormat, self.colorBeads)