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
#Requirements in this file: 3.1.2, 3.1.4, 3.1.5, 3.1.11, 3.2.7, 3.3.2
#Authors: Jacob Wakefield, Noah Zeilmann, McKenna Gates, Liam Zay

from . import app
import json
from flask import render_template, send_from_directory, request, url_for, redirect, jsonify, send_file

from lib.counting import *
from lib.stitching import *
from lib.file_util import *

"""
    Description: a template class used for defining the detection parameters
    given from the front end.
"""
class Parameters():
    def __init__(self):
        self.wantsCrushedBeads = False
        self.wantsWaterBubbles = False
        self.beadUpperBound = 0
        self.beadLowerBound = 0
        self.detectionAlgorithm = ''

detectionParams = Parameters()

countingDict = {} # global counting dictionary variable for regeneration of csv data. keys are timestamp directory names

# route for serving static resources (images/js/css)
@app.route('/resources/<path:path>')
def sendStaticResource(path):
    return send_from_directory('resources', path)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/error')
def error():
    errorMessage = request.args['errorMessage']
    return render_template('error.html',error=errorMessage)

@app.route('/uploadImages', methods=["POST"])
def uploadImagesAndConfigure():

    detectionParams.wantsCrushedBeads = True if request.args['wantsCrushed'] == 'true' else False # convert js 'bool' to python Bool
    detectionParams.detectionAlgorithm = request.args['colorAlgorithm']
    
    images = request.files.getlist("images")

    newDir = file_util.createUploadDir()
    if not file_util.checkImagesAndSaveToDirectory(images, newDir):
        return jsonify({"status": 1, "msg": "One or more of the images that were uploaded are in the incorrect format. Accepted formats: " \
                         + (", ".join(file_util.ALLOWED_IMAGE_EXTENSIONS))})

    return jsonify({"status": 0, "msg": "Success","location": newDir.replace("Server/resources/uploads","")}) # redirect to homepage

# accepts a path to the image directory to use for stitching
@app.route('/getStitchedImage/<path:directory>')
def getStitchedImage(directory):

    dirPrefix = 'Server/resources/uploads/' + directory
    stitcher = Stitching(dirPrefix + '/images/', dirPrefix + '/maps/')
    (status, statusString) = stitcher.stitchImages_Default()
    
    return render_template('stitched_single.html', status=status, statusString=statusString, directory=directory)

    #stitcher.twoRoundStitch(dirPrefix + directory + "/images/", dirPrefix + directory + "/maps/")
    #return render_template('stitched.html', direct=directory)

# accepts a path to the stitched image directory
@app.route('/getResults/<path:directory>')
def getResults(directory): 

    magLevel = HoughConfig.OBJX4 if request.args.get('maglevel') == '4x' else HoughConfig.OBJX10

    resultsDirectory = directory.split("/")[0]
    serverDirectory = 'Server/resources/uploads/' + directory

    countingDict[resultsDirectory] = Counting(serverDirectory) # save the counting object in a dictionary for regeneration of report data
    colorBeads = countingDict[resultsDirectory].getColorBeads(magLevel, detectionParams)

    return render_template('results.html', colorBeads = colorBeads, waterBeads = countingDict[resultsDirectory].waterBeads,
        crushedBeads = countingDict[resultsDirectory].crushedBeads, mapLocation = directory, resultsDirectory = resultsDirectory)

@app.route('/getResultReport/<path:directory>')
def getResultReport(directory):
    colorOutputType = request.args.get('colorOutputType') # this is the type of output we want
    resDir = request.args.get('resDir') # this is the directory we are accessing
    
    countingDict[directory].makeBeadsCSV(colorOutputType) # access the stored counting variable and regen csv data

    uploadDir = 'resources/uploads/' + resDir

    return send_file(uploadDir + '/results/beads.csv', as_attachment=True)