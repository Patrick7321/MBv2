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

# Authors: Gattlin Walker

import cv2
import numpy as np
import math

"""
	Finds the closest color associated with a contour
	@param img -  image the contours are found
	@param conotour - a given contour found on the image.
"""
def getClosestColor(img, contour):
	# colors given in LAB color space
	colors = [
		("red", (136, 208, 195)),
		("green", (224, 42, 211)),
		("blue", (82, 207, 20)),
		("black", (0, 128, 128)),
		("yellow", (248, 106, 223)),
		("darkblue", (10, 157, 86)),
		("gray", (104, 128, 128)),
		("darkgray", (76, 128, 128)),
		("white", (255, 128, 128)),
		("lightblue", (203, 117, 100)),
		]

	mask = np.zeros(img.shape[:2], dtype="uint8")
	cv2.drawContours(mask, [contour], -1, 255, -1)
	mean = cv2.mean(img, mask=mask)

	closestPair = ('color', math.inf)

	for key, value in colors:
		distance = euclidean(value, mean[:3])
		if distance < closestPair[1]:
			closestPair = (key, distance)

	return closestPair[0]

"""
	Euclidean distance formula to find the similarity between two entries
	@param entry1 - first entry being compared
	@param entry2 - second entry being compared
	@return the distance between the two entries
"""
def euclidean(entry1, entry2):
	distance = 0

	for i in range(len(entry1)):
		distance += (entry1[i] - entry2[i]) ** 2

	return distance ** 0.5

"""
	Determines if the color is valid and not a blacklisted color
	@param color - string of the given color
	@return - boolean if the color is not in the colors to ignore
"""
def validColor(color):
	colorsToIgnore = ['darkgray', 'darkblue', 'black', 'white']
	return color not in colorsToIgnore