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

#Authors: Alex Peters

import cv2
import imutils
import datetime
import os
from imutils import paths
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = set(['jpg', 'jpeg'])

"""
    Description: a function that takes a directory string and returns a list of images
    @param path - a string indicating the directory on the server's filesystem to read images from 
    @return a list of opencv images
"""
def readImagesFromDirectory(path):
    imagePaths = sorted(list(imutils.paths.list_images(path)))
    images = []
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        images.append(image)
    return images

"""
    Description: a function that writes an image to a directory
    @param path - string that indicates directory to write to
    @param image - opencv image data to write to directory
    @return void
"""
def writeImage(path, image):
    cv2.imwrite(path, image)

"""
    Description: a function used to see if the uploaded file is in a valid format.
    @Param filename - name of the file being uploaded.
    @Param extensionList - set of allowed file extensions.
    @return a boolean indicating whether the image is in an acceptable format or not.
"""
def isFileAllowed(filename, extensionList):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensionList

def createUploadDir():
    # create new folder to hold users data for run
    uploadDir = 'Server/resources/uploads'
    now = datetime.datetime.now()
    newFolder = now.strftime("%Y-%m-%dT%H-%M-%S")
    newDir = uploadDir + "/" + newFolder
    os.mkdir(newDir)
    subfolders = ['images', 'videos', 'maps', 'results', 'uploads']
    for folder in subfolders:
        subDir = newDir + "/" + folder
        os.mkdir(subDir)
    return newDir
    
"""
    Description: a function that takes an array representing a set of images and a string representing a directory to write to.
                    checks if images are of the correct format and renames them to a secure filename
    @param images - array that contains a set of opencv images
    @param directory - string that specifies the directory to save images to
    @return a boolean indicating whether or not operation was successful
"""
def checkImagesAndSaveToDirectory(images, directory):
    for i in images:
        if not isFileAllowed(i.filename, ALLOWED_IMAGE_EXTENSIONS):
            return False
        imgPath = directory + "/images/" + str(secure_filename(i.filename))
        i.save(imgPath)
    return True
