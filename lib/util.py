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

#Authors: Alex Peters, Patrick Ayres

import csv
import colorsys

CSV_RGB_COLNAMES =  ['Bead Number', 'Type', 'Red Val', 'Green Val', 'Blue Val', 'X-Coord', 'Y-Coord', 'Radius']
CSV_HSV_COLNAMES = ['Bead Number', 'Type', 'Hue Val', 'Saturation Val', 'Value Val', 'X-Coord', 'Y-Coord', 'Radius']
CSV_CMYK_COLNAMES = ['Bead Number', 'Type', 'Cyan Val', 'Magenta Val', 'Yellow Val', 'Black Val', 'X-Coord', 'Y-Coord', 'Radius']
CSV_GRAYSCALE_COLNAMES = ['Bead Number', 'Type', 'Grayscale Val', 'X-Coord', 'Y-Coord', 'Radius']

"""
    Description: function that takes beadinfo and creates a csv with varying types of color output data
    @param colorFormat: a string that is either 'rgb', 'hsv', 'cmyk', or 'grayscale'
    @return void, writes file directly from class attributes
""" 
def makeBeadsCSV(filepath, colorFormat, colorBeads, crushedBeads, waterBeads): 

    colNames = CSV_RGB_COLNAMES # RGB will be selected by default. these values will change if the colorFormat value matches below
    writeFunc = writeOutputRgb

    if colorFormat == 'hsv':
        colNames = CSV_HSV_COLNAMES
        writeFunc = writeOutputHsv
    elif colorFormat == 'cmyk': 
        colNames = CSV_CMYK_COLNAMES
        writeFunc = writeOutputCmyk
    elif colorFormat == 'grayscale':
        colNames = CSV_GRAYSCALE_COLNAMES
        writeFunc = writeOutputGrayscale
    
    with open(filepath, mode='w', newline='') as beadFile:
        writer = csv.writer(beadFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(colNames)
        writeFunc(writer, colorBeads) 
        addCrushedBeads(writer, colorFormat, crushedBeads)
        addWaterBeads(writer, colorFormat, waterBeads)

"""
    Description: a function that writes the color data to CSV in RGB format
    @param writer - the writer, preconfigured for the output file
    @param colorBeads - an array containing bead data from scan
    @return void
"""
def writeOutputRgb(writer, colorBeads): 
    i = 1
    for bead in colorBeads:
        r = bead[0][0]; g = bead[0][1]; b = bead[0][2]

        x = bead[2][0]; y = bead[2][1]
        radius = bead[2][2]
        
        writer.writerow([i, "Bead", r, g, b, x, y, radius]) # row is written with beadNum, r, g, b, x, y, radius
        i += 1

"""
    Description: a function that writes the color data to CSV in HSV format
    @param writer - the writer, preconfigured for the output file
    @param colorBeads - an array containing bead data from scan
    @return void
"""
def writeOutputHsv(writer, colorBeads): 
    i = 1
    for bead in colorBeads: 
        hsv = colorsys.rgb_to_hsv(bead[0][0]/255, bead[0][1]/255, bead[0][2]/255) # here, the colorsys conversion function expects values between 0-1 for rgb
        h = hsv[0]; s = hsv[1]; v = hsv[2] # the returned values are placed in an array in the order h, s, v

        x = bead[2][0]; y = bead[2][1]
        radius = bead[2][2]

        writer.writerow([i, "Bead", h, s, v, x, y, radius]) # row is written with beadNum, h, s, v, x, y, radius
        i += 1

"""
    Description: a function that writes the color data to CSV in CMYK format
    @param writer - the writer, preconfigured for the output file
    @param colorBeads - an array containing bead data from scan
    @return void
"""
def writeOutputCmyk(writer, colorBeads): 
    i = 1
    for bead in colorBeads: 
        cmyk = rgbToCmyk(bead[0][0], bead[0][1], bead[0][2])
        C = cmyk[0]; M = cmyk[1]; Y = cmyk[2]; K = cmyk[3] # the returned values are placed in an array in the order c, m, y, k

        x = bead[2][0]; y = bead[2][1]
        radius = bead[2][2]

        writer.writerow([i, "Bead", C, M, Y, K, x, y, radius]) # row is written with beadNum, c, m, y, k, x, y, radius
        i += 1

"""
    Description: a function that writes the color data to CSV in Grayscale format
    @param writer - the writer, preconfigured for the output file
    @param colorBeads - an array containing bead data from scan
    @return void
"""
def writeOutputGrayscale(writer, colorBeads):
    i = 1
    for bead in colorBeads:
        grayscaleValue = listAverage(bead[0])

        x = bead[2][0]; y = bead[2][1]
        radius = bead[2][2]
        
        writer.writerow([i, "Bead",  grayscaleValue, x, y, radius]) # row is written with beadNum, grayscaleValue, x, y, radius
        i += 1

"""
    Description: a function that sums the values in a list
    @param lst - the list to average
    @return the average of values in the list
"""
def listAverage(lst): 
    return sum(lst) / len(lst)

"""
    Description: a function that takes an r, g, and b value and returns the corresponding CMYK values
    @param r - an int representing red 
    @param g - an int representing green
    @param b - an int representing blue
    @return a tuple of length four representing (C, M, Y, K) values
"""
def rgbToCmyk(r,g,b):
    cmyk_scale = 100

    if (r + g + b) == 0: # bead is black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - (r / 255.)
    m = 1 - (g / 255.)
    y = 1 - (b / 255.)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) # / (1 - min_cmy)
    m = (m - min_cmy) # / (1 - min_cmy)
    y = (y - min_cmy) # / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale

"""
    Description: a function that writes detected crushed beads to the output file
    @param writer - the writer, preconfigured for the output file
    @param colorFormat - a string representing the selected color format
    @param crushedBeads - a list of detected crushed beads during detection
    @return void
"""
def addCrushedBeads(writer, colorFormat, crushedBeads):

    for bead in crushedBeads:
        x = bead[2][0]; y = bead[2][1];
        r = bead[2][2];

        if colorFormat == 'hsv':
            writer.writerow(["N/A", "Crushed Bead", "N/A", "N/A", "N/A", x, y, r])
        elif colorFormat == 'cmyk':
            writer.writerow(["N/A", "Crushed Bead", "N/A", "N/A", "N/A", "N/A", x, y, r]) 
        elif colorFormat == 'grayscale':
            writer.writerow(["N/A", "Crushed Bead", "N/A", x, y, r])
        elif colorFormat == 'rgb':
            writer.writerow(["N/A", "Crushed Bead", "N/A", "N/A", "N/A", x, y, r])

"""
    Description: a function that writes detected water bubbles to the output file
    @param writer - the writer, preconfigured for the output file
    @param colorFormat - a string representing the selected color format
    @param crushedBeads - a list of detected water bubbles during detection
    @return void
"""
def addWaterBeads(writer, colorFormat, waterBeads):
    
    for bead in waterBeads:
        x = bead[2][0]; y = bead[2][1];
        r = bead[2][2];

        if colorFormat == 'hsv':
            writer.writerow(["N/A", "Water Bubble", "N/A", "N/A", "N/A", x, y, r])
        elif colorFormat == 'cmyk':
            writer.writerow(["N/A", "Water Bubble", "N/A", "N/A", "N/A", "N/A", x, y, r]) 
        elif colorFormat == 'grayscale':
            writer.writerow(["N/A", "Water Bubble", "N/A", x, y, r])
        elif colorFormat == 'rgb':
            writer.writerow(["N/A", "Water Bubble", "N/A", "N/A", "N/A", x, y, r])


        

