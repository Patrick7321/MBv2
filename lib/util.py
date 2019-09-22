import csv
import colorsys

CSV_RGB_COLNAMES =  ['Bead Number', 'Red Val', 'Green Val', 'Blue Val', 'X-Coord', 'Y-Coord', 'Radius']
CSV_HSV_COLNAMES = ['Bead Number', 'Hue Val', 'Saturation Val', 'Value Val', 'X-Coord', 'Y-Coord', 'Radius']
CSV_CMYK_COLNAMES = ['Bead Number', 'Cyan Val', 'Magenta Val', 'Yellow Val', 'Black Val', 'X-Coord', 'Y-Coord', 'Radius']

"""
    Description: function that takes beadinfo and creates a csv with varying types of color output data
    @param colorFormat: a string that is either 'rgb', 'hsv', 'cmyk', or 'grayscale'
    @return void, writes file directly from class attributes
""" 
def makeBeadsCSV(filepath, colorFormat, colorBeads): 

    colNames = CSV_RGB_COLNAMES
    writeFunc = writeOutputRgb

    if colorFormat == 'hsv':
        colNames = CSV_HSV_COLNAMES
        writeFunc = writeOutputHsv
    elif colorFormat == 'cmyk': 
        colNames = CSV_CMYK_COLNAMES
        writeFunc = writeOutputCmyk
    
    with open(filepath, mode='w', newline='') as beadFile:
        writer = csv.writer(beadFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(colNames)
        writeFunc(writer, colorBeads)


def writeOutputRgb(writer, colorBeads): 
    i = 1
    for bead in colorBeads:
        r = bead[0][0]; g = bead[0][1]; b = bead[0][2]

        x = bead[2][0]; y = bead[2][1]
        radius = bead[2][2]
        
        writer.writerow([i, r, g, b, x, y, radius]) # row is written with beadNum, r, g, b, x, y, radius
        i += 1

def writeOutputHsv(writer, colorBeads): 
    i = 1
    for bead in colorBeads: 
        hsv = rgbToHsv(bead[0][0]/255, bead[0][1]/255, bead[0][2]/255) # here, the colorsys conversion function expects values between 0-1 for rgb
        h = hsv[0]; s = hsv[1]; v = hsv[2] # the returned values are placed in an array in the order h, s, v

        x = bead[2][0]; y = bead[2][1]
        radius = bead[2][2]

        writer.writerow([i, h, s, v, x, y, radius]) # row is written with beadNum, h, s, v, x, y, radius
        i += 1

def writeOutputCmyk(writer, colorBeads): 
    i = 1
    for bead in colorBeads: 
        cmyk = rgbToCmyk(bead[0][0], bead[0][1], bead[0][2]) # here, the colorsys conversion function expects values between 0-1 for rgb
        c = cmyk[0]; m = cmyk[1]; y = cmyk[2]; k = cmyk[3] # the returned values are placed in an array in the order c, m, y, k

        x = bead[2][0]; y = bead[2][1]
        radius = bead[2][2]

        writer.writerow([i, c, m, y, k, x, y, radius]) # row is written with beadNum, h, s, v, x, y, radius
        i += 1

def rgbToHsv(r, g, b):
    hsv = colorsys.rgb_to_hsv(r, g, b)
    return hsv

# TODO: am i allowed to use this code? i copy/pasted it from stack overflow, 
# more specifically: 
# https://stackoverflow.com/questions/14088375/how-can-i-convert-rgb-to-cmyk-and-vice-versa-in-python/30078860
# how do i give the author credit?
def rgbToCmyk(r,g,b):
    cmyk_scale = 100

    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / 255.
    m = 1 - g / 255.
    y = 1 - b / 255.

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale