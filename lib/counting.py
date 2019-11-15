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
import datetime
from enum import Enum
from os import listdir, path
from . import util
from . import colorLabeler

"""
    Description: an enum class to handle the HoughCircle configuration values that are used in cv2.HoughCircles().
"""
class HoughConfig(Enum):

    # 4x magnification
    OBJX4 = { "dp": 1,"minDist": 40,"param1": 50,"param2": 55,"minRadius": 0,"maxRadius": 75 }

    # 10x magnification
    OBJX10 = { "dp": 1,"minDist": 60,"param1": 65,"param2": 68,"minRadius": 0,"maxRadius": 125 }

    DEFAULT = { "dp": 1,"minDist": 0,"param1": 50,"param2": 30,"minRadius": 0,"maxRadius": 125 }

"""
    Description: a class to deal with counting microbeads in a stitched image.
"""
class Counting:

    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.grayScaleMap = cv2.imread(imagePath,0) # create grayscale cv2 img
        self.colorMap = cv2.imread(imagePath) # create color cv2 img
        self.labMap = cv2.cvtColor(self.colorMap, cv2.COLOR_BGR2Lab)
        self.colorBeads = []
        self.waterBeads = []
        self.partialBeads = []
        self.crushedBeads = []

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
        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,
                                    dp=houghConfig["dp"],
                                    minDist=detectionParams.minDist,
                                    param1=houghConfig["param1"],
                                    param2=detectionParams.sensitivity,
                                    minRadius=detectionParams.minRadius,
                                    maxRadius=detectionParams.maxRadius)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # i[0] is x coordinate, i[1] is y coordinate, i[2] is radius
                # draw the outer circle
                cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

                partial = self.checkPartial(i)

                if detectionParams.detectionAlgorithm == "avg":
                    color = self.getAverageColor(i)
                elif detectionParams.detectionAlgorithm == "mid":
                    color = self.getMiddleColor(i)
                elif detectionParams.detectionAlgorithm == "corner":
                    color = self.getFourQuadrantColor(i)
                elif detectionParams.detectionAlgorithm == "rad":
                    color = self.getRadiusAverageColor(i)


                if partial:
                    self.partialBeads.append(color)
                elif(color[1] == 'bead'): # if the bead is a water bead, leave it out.
                    self.colorBeads.append(color)
                    result.append(color)
                else:
                    self.waterBeads.append(color)

        if detectionParams.wantsCrushedBeads: # if the user wants to detect crushed beads.
            self.getCrushedBeads(cimg)

        imagePath = '/'.join(self.imagePath.split('/')[:-2]) + '/results/'
        imagePath += 'result_image.jpg'#+ str(fileNum) +'.jpg'
        cv2.imwrite(imagePath, cimg)

        return result

    """
        Description: a function that takes a cicle's RGB values and returns if it is water or not
        @param RGB - tuple containing the average red, green, and blue values of a circle
        @return a boolean that will be True if the circle is water
    """
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
    Description: does preprocessing on the image map to find the crushed beads.
    @param image - image that will have the final results of the counting
    """
    def getCrushedBeads(self, image):
        color = self.__removeKnownObjects(image)

        # makes background an even white color
        minBg = (235, 235, 235)
        maxBg = (255, 255, 255)
        self.__removeImgAspect(color, minBg, maxBg)

        # removes black edges caused by stitching
        minBlack = (0, 0, 0)
        maxBlack = (10, 10, 10)
        self.__removeImgAspect(color, minBlack, maxBlack)

        lab = cv2.cvtColor(color, cv2.COLOR_BGR2LAB)

        # removes black borders
        minBorder = (0, 0, 0)
        maxBorder = (180, 190, 130)
        self.__removeImgAspect(lab, minBorder, maxBorder, drawing=color)

        contours = self.__findContours(color)
        cl = colorLabeler.ColorLabeler()

        imageY = image.shape[0]
        imageX = image.shape[1]
        for c in contours:
            color_label = cl.label(self.labMap, c)
            if color_label not in cl.colorsToIgnore:
                M = cv2.moments(c)
                if M['m00'] > 0:
                    cX = int((M["m10"] / M["m00"]))
                    cY = int((M["m01"] / M["m00"]))
                    if cX >= imageX - 100 or cY >= imageY - 100:
                        pass
                    else:
                        self.crushedBeads.append([[0, 0, 0], 'crushedBead', [cX, cY, 35]])
                        cv2.drawContours(image, [c], -1, (255, 0, 0), 4)
                        cv2.circle(image, (cX, cY), 2, (255, 0, 0), 3)

    def __removeKnownObjects(self, image):
        mask = np.ones(image.shape[:2], dtype="uint8")
        knownObjects = self.colorBeads + self.waterBeads + self.partialBeads

        # takes the known objects (beads and water beads) and colors them black
        # so they can be ignored when detecting the crushed beads
        for bead in knownObjects:
            cv2.circle(mask, (bead[2][0],bead[2][1]), bead[2][2], (0,0,0), -1)
            cv2.circle(mask, (bead[2][0],bead[2][1]), bead[2][2], (0,0,0), 16)

        color = cv2.bitwise_and(self.colorMap, self.colorMap, mask=mask)

        return color

    """
    Description: Gets the locations of pixels within a given bound and colors
    them white so they will not be picked up during image detection
    @param img - the image used to find the pixels withing a given range
    @param minBound - the lower bound of a pixel's color intensity
    @param maxBound - the upper bound of a pixel's color intensity
    @param drawing - an optional parameter in case the image the results need to be drawn on
                     is different than the image the range detection was performed on.
    """
    def __removeImgAspect(self, img, minBound, maxBound, drawing=None):
        # if no drawing image is given then it becomes the original img
        if drawing is None:
            drawing = img

        aspect = cv2.inRange(img, minBound, maxBound)
        imgOutput, contours, hierarchy = cv2.findContours(aspect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            cv2.drawContours(drawing, [c], -1, (255, 255, 255), -1)

    def __findContours(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (31, 31), 0)
        thresh = cv2.threshold(blur, 225, 255, cv2.THRESH_BINARY_INV)[1]
        kernel = np.ones((5,5),np.uint8)
        erosion = cv2.erode(thresh,kernel,iterations = 1)
        imgOutput, contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    """
        Description: a function that takes an array representing a circle's[x-coord of center, y-coord of center, radius]
                    and returns a list containing tuple with the bead's average RGB values of the top 10% and boolean isWater
        @param circleInfo - array that contains a circle's x and y coordinates of the center and the radius of the circle
        @param imageMap - a map (image) of the microscope images in color.
        @return a list containing tuple with average RGB values of top 10% from bead, boolean isWater, and x,y,radius value of the bead.
    """

    def checkPartial(self, circle):
        img = self.colorMap
        imgY = img.shape[0]
        imgX = img.shape[1]
        x = circle[0]
        y = circle[1]
        radius = circle[2]

        if x + radius >= imgX or y + radius >= imgY:
            return True
        else:
            return False

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
        currentTime = datetime.datetime.now()
        currentTimeString = currentTime.strftime("%Y-%m-%dT%H-%M-%S")

        if colorFormat == "rgb":
                    newPath = newPath + '/rgb_' + currentTimeString + '.csv'
        elif colorFormat == "hsv":
                    newPath = newPath + '/hsv_' + currentTimeString + '.csv'
        elif colorFormat == "cmyk":
                    newPath = newPath + '/cmyk_' + currentTimeString + '.csv'
        elif colorFormat == "grayscale":
                    newPath = newPath + '/grayscale_' + currentTimeString + '.csv'

        print(newPath, file=sys.stderr)

        util.makeBeadsCSV(newPath, colorFormat, self.colorBeads, self.crushedBeads, self.waterBeads)
        return currentTimeString