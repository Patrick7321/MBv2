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

#Requirements in this file: 3.1.6, 3.2.4, 3.2.6
#Authors: Noah Zeilmann, Josiah Carpenter

#Authors: Alex Peters

import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import sys
from PIL import Image, ExifTags
import shutil
import multiprocessing as mp
from collections import OrderedDict
import imutils
from imutils import paths
from . import file_util

"""
        Description: a class to deal with stitching images together and handling overlap of the images.
"""
class Stitching:
	def __init__(self, sourceDirectory, resultsDirectory):
		self.images = []
		self.sourceDirectory = self.setDirectory(sourceDirectory)
		self.resultsDirectory = resultsDirectory
		self.results = []

	"""
		Description: a method that stitches the images configured to this object
		@return an opencv image of the stitched image
	"""
	def stitchImages_Default(self):

		if(len(self.images) < 2):
			file_util.writeImage(self.resultsDirectory + 'result_default.jpg', self.images[0])
			return (0, 'single')

		else:
			stitcher = cv2.createStitcher(False)
			print(len(self.images))
			(status, stitched) = stitcher.stitch(self.images)

			if status != 0:
				print(status)
				blank_image = np.zeros((50, 50, 3), np.uint8)
				file_util.writeImage(self.resultsDirectory + 'result_default.jpg', blank_image)
				return (status, 'An error occured while stitching.')

			file_util.writeImage(self.resultsDirectory + 'result_default.jpg', stitched)
			return (status, 'Success.')

	"""
		Description: a function setting the directory where images are contained for this object.
				uses the file_utils file to read file recursively with imutils
		@param path - The directory in unix format
	"""
	def setDirectory(self, path):
		# Get directory of test images
		self.sourceDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", path))

		# and pass that directory into the file_util to recursively read all images from that dir
		self.images = file_util.readImagesFromDirectory(self.sourceDirectory)

	"""
		Description: a setter for the object's directory path
		@param path - a string that indicates the path to set in the object
		@return void
	"""
	def setResultsDirectory(self,path):
		self.resultsDirectory = path

