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
        self.detectionAlgorithm = 'avg'
        self.magnificationLevel = '4x'
        
        self.minDist = 10
        self.sensitivity = 50
        self.minRadius = 50
        self.maxRadius = 120

paramDict = {} 

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

    newDir = file_util.createUploadDir()

    timestamp = newDir.split("/")[3]

    paramDict[timestamp] = Parameters()
    paramDict[timestamp].wantsCrushedBeads = True if request.args['wantsCrushed'] == 'true' else False # convert js 'bool' to python Bool
    paramDict[timestamp].wantsWaterBubbles = True if request.args['wantsBubbles'] == 'true' else False
    paramDict[timestamp].detectionAlgorithm = request.args['colorAlgorithm']
    paramDict[timestamp].minRadius = int(request.args['minBead'])
    paramDict[timestamp].maxRadius = int(request.args['maxBead'])
    
    if 'maglevel' in request.args:
        paramDict[timestamp].magnificationLevel = request.args['maglevel']

    images = request.files.getlist("images")

    if not file_util.checkImagesAndSaveToDirectory(images, newDir):
        return jsonify({"status": 1, "msg": "One or more of the images that were uploaded are in the incorrect format. Accepted formats: " \
                         + (", ".join(file_util.ALLOWED_IMAGE_EXTENSIONS))})

    return jsonify({"status": 0, "msg": "Success","location": newDir.replace("Server/resources/uploads","")}) # redirect to homepage

# accepts a path to the image directory to use for stitching
@app.route('/getStitchedImage/<path:stitchDirectory>')
def getStitchedImage(stitchDirectory):

    dirPrefix = 'Server/resources/uploads/' + stitchDirectory
    stitcher = Stitching(dirPrefix + '/images/', dirPrefix + '/maps/')
    (status, statusString) = stitcher.stitchImages_Default()

    if(statusString == "single"):
        return redirect(url_for('getResults', directory = stitchDirectory + '/maps/result_default.jpg'))
    else:
        return render_template('stitched_single.html', status=status, statusString=statusString, directory=stitchDirectory)

    #stitcher.twoRoundStitch(dirPrefix + directory + "/images/", dirPrefix + directory + "/maps/")
    #return render_template('stitched.html', direct=directory)

# accepts a path to the stitched image directory
@app.route('/getResults/<path:directory>')
def getResults(directory):

    resultsDirectory = directory.split("/")[0]

    countingParameters = Parameters()
    if resultsDirectory in paramDict:
        countingParameters = paramDict[resultsDirectory]
    else: 
        paramDict[resultsDirectory] = countingParameters

    magLevel = ''
    if request.args.get('maglevel') == '4x' or countingParameters.magnificationLevel == '4x':
        magLevel = HoughConfig.OBJX4
    else:
        magLevel = HoughConfig.OBJX10

    serverDirectory = 'Server/resources/uploads/' + directory
    countingDict[resultsDirectory] = Counting(serverDirectory) # save the counting object in a dictionary for regeneration of report data

    colorBeads = countingDict[resultsDirectory].getColorBeads(magLevel, countingParameters)

    return render_template('results.html', colorBeads = colorBeads, waterBeads = countingDict[resultsDirectory].waterBeads,
        crushedBeads = countingDict[resultsDirectory].crushedBeads, mapLocation = directory, resultsDirectory = resultsDirectory, 
                minDist = countingParameters.minDist,
                sensitivity = countingParameters.sensitivity,
                minRadius = countingParameters.minRadius,
                maxRadius = countingParameters.maxRadius
        )

@app.route('/setParameters', methods=['POST'])
def setParameters():
    try:
        jsonData = request.get_json()

        timestamp = jsonData['timestamp']

        countingParameters = Parameters()
        if timestamp in paramDict:
            countingParameters = paramDict[timestamp]
        else: 
            paramDict[timestamp] = countingParameters

        countingParameters.minDist = int(jsonData['minDist'])
        countingParameters.sensitivity = int(jsonData['sensitivity'])
        countingParameters.minRadius = int(jsonData['minRadius'])
        countingParameters.maxRadius = int(jsonData['maxRadius'])

        return jsonify({'status': 0, 'statusString': 'Parameters successfully set'})

    except Exception as e: 
        return jsonify({'status': 1, 'statusString': 'An Error occurred setting parameters'})

@app.route('/getResultReport/<path:directory>')
def getResultReport(directory):
    colorOutputType = request.args.get('colorOutputType') # this is the type of output we want
    resDir = request.args.get('resDir') # this is the directory we are accessing
    uploadDir = 'resources/uploads/' + resDir

    csvTimestamp = countingDict[directory].makeBeadsCSV(colorOutputType) # access the stored counting variable and regen csv data

    return send_file(uploadDir + '/results/' + colorOutputType + '_' + csvTimestamp + '.csv', as_attachment=True)