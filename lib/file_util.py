import cv2
import imutils
import datetime
import os
from imutils import paths
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = set(['jpg', 'jpeg'])

# method takes a relative (or an absolute? idk i havent tested it), recursively finds all images within it, and
# converts them to cv2 images and combines them into an array.
# returns an array of images found in the specified directory
def readImagesFromDirectory(path):
    imagePaths = sorted(list(imutils.paths.list_images(path)))
    images = []
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        # print(image.shape)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # print(image.shape)
        # image = image.astype('uint8')
        images.append(image)
    return images

# method takes a path and image and writes the image to that path
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
    
def checkImagesAndSaveToDirectory(images, directory):
    for i in images:
        if not isFileAllowed(i.filename, ALLOWED_IMAGE_EXTENSIONS):
            return False
        imgPath = directory + "/images/" + str(secure_filename(i.filename))
        i.save(imgPath)
    return True
