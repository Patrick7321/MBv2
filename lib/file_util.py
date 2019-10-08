import cv2
import imutils
from imutils import paths

# method takes a relative (or an absolute? idk i havent tested it), recursively finds all images within it, and
# converts them to cv2 images and combines them into an array.
# returns an array of images found in the specified directory
def readImagesFromDirectory(path):
    imagePaths = sorted(list(imutils.paths.list_images(path)))
    images = []
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        images.append(image)
    return images

# method takes a path and image and writes the image to that path
def writeImage(path, image):
    cv2.imwrite(path, image)