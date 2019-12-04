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
#Authors: Gattlin Walker, Patrick Ayres, Alex Peters
import unittest
import os
import csv
import colorsys
import cv2
import coverage

from lib.counting import *
from lib.util import rgbToCmyk

from Server.routes import *





class TestBeadSize(unittest.TestCase):

    def setUp(self):
        self.test_count = Counting('test/test_bead_size_directory/maps/result_default.jpg')
        self.test_params = Parameters()

    #FR. 1-1
    def test_beads_within_bounds(self):
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        self.assertEqual(len(beads), 4)

    #FR. 1-2
    def test_no_small_beads(self):
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 110
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        self.assertEqual(len(beads), 0)

    #FR. 1-3
    def test_no_big_beads(self):
        self.test_params.maxRadius = 80
        self.test_params.minRadius = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        self.assertEqual(len(beads), 0)

    #FR. 1-4
    def test_upper_bound_smaller_than_lower_bound(self):
        self.test_params.maxRadius = 50
        self.test_params.minRadius = 80
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        #this should return an error

    #FR. 1-5
    def test_upper_bound_smaller_than_lower_default(self):
        self.test_params.maxRadius = 10
        self.test_params.minRadius = 30
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        #this should return an error

    #FR. 1-6
    def test_lower_bound_larger_than_upper_default(self):
        self.test_params.maxRadius = 80
        self.test_params.minRadius = 100
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        #this should return an error

    #FR. 1-7
    def test_default_size_bounds(self):
        self.test_params.maxRadius = 80;
        self.test_params.minRadius = 30;
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        self.assertEqual(len(beads), 0)

    #FR. 1-8
    def test_upper_bound_equal_to_lower_bound(self):
        self.test_params.maxRadius = 40;
        self.test_params.minRadius = 40;
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        #this should return an error

    #FR. 1-9
    #Error - Video

    #FR. 1-10
    #Error - Video

    #FR. 1-11
    #Error - Video


class TestCrushedBeads(unittest.TestCase):

    def setUp(self):
        self.test_params = Parameters()

    #FR. 2-1
    def test_single_crushed_bead(self):
        test_count = Counting('test/test_crushed_bead_directory/images/one_crushed.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.wantsCrushedBeads = True
        self.test_params.minRadius = 55
        self.test_params.maxRadius = 100
        self.test_params.minRadius = 35
        self.test_params.detectionAlgorithm = "mid"

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX10.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 2)

    #FR. 2-2
    def test_no_crushed_beads(self):
        test_count = Counting('test/test_crushed_bead_directory/images/no_crushed.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.wantsCrushedBeads = True
        self.test_params.minRadius = 30
        self.test_params.maxRadius = 60
        self.test_params.detectionAlgorithm = "mid"

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX4.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 0)

    #FR. 2-3
    def test_multiple_crushed_bead(self):
        test_count = Counting('test/test_crushed_bead_directory/images/multiple_crushed.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.wantsCrushedBeads = True
        self.test_params.minRadius = 30
        self.test_params.maxRadius = 60
        self.test_params.detectionAlgorithm = "mid"

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX4.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 4)

    #FR. 2-4
    def test_crushed_bead_off_with_crushed(self):
        test_count = Counting('test/test_crushed_bead_directory/images/multiple_crushed.jpg')

        self.test_params.beadUpperBound = 40;
        self.test_params.beadLowerBound = 60;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = False

        test_count.getColorBeads(HoughConfig.OBJX4, self.test_params)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 0)

    #FR. 2-5
    def test_crushed_bead_off_without_crushed(self):
        test_count = Counting('test/test_crushed_bead_directory/images/no_crushed.jpg')

        self.test_params.beadUpperBound = 40;
        self.test_params.beadLowerBound = 60;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = False

        test_count.getColorBeads(HoughConfig.OBJX4, self.test_params)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 0)

    #FR. 2-6
    # Tests to make sure the black edges from a stitched image do not affect
    # the detection results
    def test_crushed_bead_with_stitched_image(self):
        test_count = Counting('test/test_crushed_bead_directory/maps/stitched_map.jpg')

        self.test_params.beadUpperBound = 20;
        self.test_params.beadLowerBound = 60;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = True
        self.test_params.wantsWaterBubbles = True
        self.test_params.sensitivity = 50
        self.test_params.minRadius = 20

        test_count.getColorBeads(HoughConfig.OBJX4, self.test_params)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 5)

    #FR. 2-7
    def test_crushed_bead_with_black_borders(self):
        test_count = Counting('test/test_crushed_bead_directory/images/black_borders.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.beadUpperBound = 20;
        self.test_params.beadLowerBound = 60;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = True
        self.test_params.sensitivity = 50
        self.test_params.minRadius = 20

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX4.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 4)

    #FR. 2-8
    def test_crushed_bead_with_black_borders_no_crushed_beads(self):
        test_count = Counting('test/test_crushed_bead_directory/images/borders_with_no_crushed.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.beadUpperBound = 20;
        self.test_params.beadLowerBound = 60;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = True
        self.test_params.sensitivity = 50
        self.test_params.minRadius = 20

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX4.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 0)

    #FR. 2-9
    def test_crushed_bead_with_stitched_image_no_crushed_beads(self):
        test_count = Counting('test/test_crushed_bead_directory/maps/stitched_no_crushed.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.beadUpperBound = 20;
        self.test_params.beadLowerBound = 50;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = True
        self.test_params.sensitivity = 50
        self.test_params.minRadius = 20

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX4.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 0)

    #FR. 2-10
    def test_crushed_beads_with_black_borders_and_edges_no_crushed_beads(self):
        test_count = Counting('test/test_crushed_bead_directory/maps/stitched_no_crushed.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.beadUpperBound = 20;
        self.test_params.beadLowerBound = 50;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = True
        self.test_params.sensitivity = 50
        self.test_params.minRadius = 20

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX4.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 0)

    #FR. 2-11 test/test_crushed_bead_directory/images/multiple_colors.jpg
    def test_crushed_bead_with_colored_crushed_areas(self):
        test_count = Counting('test/test_crushed_bead_directory/images/multiple_colors.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.beadUpperBound = 20;
        self.test_params.beadLowerBound = 40;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = True
        self.test_params.sensitivity = 40
        self.test_params.minRadius = 20

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX4.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 1)

    #FR. 2-12
    def test_cracked_beads_with_crushed(self):
        test_count = Counting('test/test_crushed_bead_directory/images/cracked_beads.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.beadUpperBound = 20;
        self.test_params.beadLowerBound = 60;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = True
        self.test_params.sensitivity = 40
        self.test_params.minRadius = 20

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX4.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 2)

    #FR. 2-13
    def test_cracked_beads_without_crushed(self):
        test_count = Counting('test/test_crushed_bead_directory/images/cracked_beads.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.beadUpperBound = 20;
        self.test_params.beadLowerBound = 60;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = False
        self.test_params.sensitivity = 50
        self.test_params.minRadius = 20

        test_count.getColorBeads(HoughConfig.OBJX4, self.test_params)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 0)

    #FR. 2-14
    def test_crushed_beads_with_black_borders_and_edges(self):
        test_count = Counting('test/test_crushed_bead_directory/maps/black_borders_and_edges.jpg')
        cimg = cv2.cvtColor(test_count.grayScaleMap, cv2.COLOR_GRAY2BGR)

        self.test_params.beadUpperBound = 20;
        self.test_params.beadLowerBound = 60;
        self.test_params.detectionAlgorithm = "mid"
        self.test_params.wantsCrushedBeads = True
        self.test_params.sensitivity = 50
        self.test_params.minRadius = 20

        test_count.getCrushedBeads(cimg, self.test_params, HoughConfig.OBJX4.value)

        crushedCount = len(test_count.crushedBeads)
        self.assertEqual(crushedCount, 4)


class TestWaterBubble(unittest.TestCase):

    def setUp(self):
        self.one_bubble_filename = 'test/test_water_bubble_directory/single/single.jpg'
        self.multiple_bubble_filename = 'test/test_water_bubble_directory/multiple/multiple.jpg'
        self.no_bubble_filename = 'test/test_water_bubble_directory/none/none.jpg'

        self.test_params = Parameters()
        self.setUpParameters()

    def setUpParameters(self):
        self.test_params.detectionAlgorithm = 'mid'
        self.test_params.wantsWaterBubbles = True
        self.test_params.minDist = 40
        self.test_params.sensitivity = 55
        self.test_params.minRadius = 0
        self.test_params.maxRadius = 75

    #FR. 3-1
    def test_water_bubble(self):
        counter = Counting(self.one_bubble_filename)
        beads = counter.getColorBeads(HoughConfig.OBJX10, self.test_params)
        self.assertEqual(len(counter.waterBeads), 1)

    #FR. 3-2
    def test_no_water_bubble(self):
        counter = Counting(self.no_bubble_filename)
        beads = counter.getColorBeads(HoughConfig.OBJX10, self.test_params)
        self.assertEqual(len(counter.waterBeads), 0)

    #FR. 3-3
    def test_multiple_water_bubbles(self):
        counter = Counting(self.multiple_bubble_filename)
        beads = counter.getColorBeads(HoughConfig.OBJX10, self.test_params)
        self.assertEqual(len(counter.waterBeads), 3)

    #FR. 3-4
    def test_water_bubble_off_with_bubble(self):
        self.test_params.wantsWaterBubbles = False
        counter = Counting(self.one_bubble_filename)
        beads = counter.getColorBeads(HoughConfig.OBJX10, self.test_params)
        self.assertEqual(len(counter.waterBeads), 0)

    #FR. 3-5
    def test_water_bubble_off_without_bubble(self):
        self.test_params.wantsWaterBubbles = False
        counter = Counting(self.no_bubble_filename)
        beads = counter.getColorBeads(HoughConfig.OBJX10, self.test_params)
        self.assertEqual(len(counter.waterBeads), 0)


class TestPartialBead(unittest.TestCase):


    def setUp(self):
        self.MARGIN_OF_ERROR = .95
        self.test_params = Parameters()


    #FR. 4-1
    def test_single_partial_bead(self):
        self.test_count = Counting('test/test_partial_bead_directory/single/maps/result_default.jpg')
        self.test_params.minDist = 40
        self.test_params.sensitivity = 40
        self.test_params.minRadius = 50
        self.test_params.maxRadius = 125
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        self.assertEqual(len(beads), 2)


    #FR. 4-2
    def test_no_partial_beads(self):
        self.test_count = Counting('test/test_bead_size_directory/maps/result_default.jpg')
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        self.assertEqual(len(beads), 4)

    #FR. 4-3
    def test_multiple_partial_bead(self):
        self.test_count = Counting('test/test_partial_bead_directory/multiple/maps/result_default.jpg')
        self.test_params.minDist = 40
        self.test_params.sensitivity = 35
        self.test_params.minRadius = 10
        self.test_params.maxRadius = 120
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        actual_count = 67
        self.assertTrue(len(beads) >= round(actual_count * self.MARGIN_OF_ERROR) and len(beads) <= round(actual_count / self.MARGIN_OF_ERROR))

    #FR. 4-4
    def test_partial_bead_true_edge_major_majority(self):
        pass

    #FR. 4-5
    def test_partial_bead_true_edge_minor_majority(self):
        pass

    #FR. 4-6
    def test_partial_bead_true_edge_minority(self):
        pass

    #FR. 4-7
    def test_partial_bead_false_top_right_edge(self):
        pass

    #FR. 4-8
    def test_partial_bead_false_top_left_edge(self):
        pass

    #FR. 4-9
    def test_partial_bead_false_bottom_left_edge(self):
        pass

    #FR. 4-10
    def test_partial_bead_false_bottom_right_edge(self):
        pass



class TestCSV(unittest.TestCase):

    def setUp(self):
        self.test_params = Parameters()

    #FR. 5-1
    def test_csv_rows(self):
        self.test_count = Counting('test/test_csv_directory/maps/result_default.jpg')
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        file_timestamp = self.test_count.makeBeadsCSV("rgb")
        csv_file = open('test/test_csv_directory/results/rgb_' + file_timestamp + '.csv', 'r')
        row_count = sum(1 for row in csv_file)
        csv_file.close()
        self.assertEqual(row_count, 5)

    #FR. 5-2
    def test_csv_type_col(self):
        self.test_count = Counting('test/test_csv_directory/maps/result_default.jpg')
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        file_timestamp = self.test_count.makeBeadsCSV("rgb")
        csv_file = open('test/test_csv_directory/results/rgb_' + file_timestamp + '.csv', 'r')
        row_count = sum(1 for row in csv_file)
        csv_file.close()
        os.remove('test/test_csv_directory/results/rgb_' + file_timestamp + '.csv')
        self.assertEqual(row_count, len(beads) + 1)

    #FR. 5-3
    def test_rgb_csv(self):
        self.test_count = Counting('test/test_csv_directory/maps/result_default.jpg')
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        file_timestamp = self.test_count.makeBeadsCSV("rgb")
        csv_file = open('test/test_csv_directory/results/rgb_' + file_timestamp + '.csv', 'r')
        data = list(csv.reader(csv_file))

        correct_file = True
        for i in range(len(beads)):
            bead_color = beads[i][0]
            file_color = [float(data[i+1][2]), float(data[i+1][3]), float(data[i+1][4])]

            if(bead_color != file_color):
                correct_file = False


        csv_file.close()
        os.remove('test/test_csv_directory/results/rgb_' + file_timestamp + '.csv')
        self.assertTrue(correct_file)

    #FR. 5-4
    def test_hsv_csv(self):
        self.test_count = Counting('test/test_csv_directory/maps/result_default.jpg')
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        file_timestamp = self.test_count.makeBeadsCSV("hsv")
        csv_file = open('test/test_csv_directory/results/hsv_' + file_timestamp + '.csv', 'r')
        data = list(csv.reader(csv_file))

        correct_file = True
        for i in range(len(beads)):
            bead_color = beads[i][0]
            hsv = colorsys.rgb_to_hsv(bead_color[0]/255, bead_color[1]/255, bead_color[2]/255)
            file_color = (float(data[i+1][2]), float(data[i+1][3]), float(data[i+1][4]))

            if(hsv != file_color):
                correct_file = False


        csv_file.close()
        os.remove('test/test_csv_directory/results/hsv_' + file_timestamp + '.csv')
        self.assertTrue(correct_file)

    #FR. 5-5
    def test_cmyk_csv(self):
        self.test_count = Counting('test/test_csv_directory/maps/result_default.jpg')
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        file_timestamp = self.test_count.makeBeadsCSV("cmyk")
        csv_file = open('test/test_csv_directory/results/cmyk_' + file_timestamp + '.csv', 'r')
        data = list(csv.reader(csv_file))

        correct_file = True
        for i in range(len(beads)):
            bead_color = beads[i][0]
            c, m, y, k = rgbToCmyk(bead_color[0], bead_color[1], bead_color[2])
            cmyk = [c, m, y, k]
            file_color = [float(data[i+1][2]), float(data[i+1][3]), float(data[i+1][4]), float(data[i+1][5])]

            if(cmyk != file_color):
                correct_file = False


        csv_file.close()
        os.remove('test/test_csv_directory/results/cmyk_' + file_timestamp + '.csv')
        self.assertTrue(correct_file)

    #FR. 5-6
    def test_grayscale_csv(self):
        self.test_count = Counting('test/test_csv_directory/maps/result_default.jpg')
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)
        file_timestamp = self.test_count.makeBeadsCSV("grayscale")
        csv_file = open('test/test_csv_directory/results/grayscale_' + file_timestamp + '.csv', 'r')
        data = list(csv.reader(csv_file))

        correct_file = True
        for i in range(len(beads)):
            bead_color = beads[i][0]
            grayscale = [sum(bead_color) / len(bead_color)]
            file_color = [float(data[i+1][2])]

            if(grayscale != file_color):
                correct_file = False


        csv_file.close()
        os.remove('test/test_csv_directory/results/grayscale_' + file_timestamp + '.csv')
        self.assertTrue(correct_file)

    #FR. 5-7
    def test_invalid_stich(self):
        pass

class TestColorAlgorithms(unittest.TestCase):

    def setUp(self):
        self.test_count = Counting('test/test_color_algorithm_directory/maps/result_default.jpg')
        self.test_params = Parameters()

    #FR. 6-1
    def test_default_color_algorithm(self):
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)

        img = self.test_count.grayScaleMap
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        blur = cv2.GaussianBlur(img,(7,7),0)

        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,
                                    dp=1,
                                    minDist=self.test_params.minDist,
                                    param1=50,
                                    param2=self.test_params.sensitivity,
                                    minRadius=self.test_params.minRadius,
                                    maxRadius=self.test_params.maxRadius)
        circles = np.uint16(np.around(circles))

        circle_list = []
        for i in circles[0,:]:
            actual_color = self.test_count.getMiddleColor(i)
            circle_list.append(actual_color)

        correct_color = True
        for i in range(len(beads)):
            calculated_color = beads[i][0]
            actual_color = circle_list[i][0]

            if(calculated_color != actual_color):
                correct_color = False

        self.assertTrue(correct_color)



    #FR. 6-2
    def test_average_color_algorithm(self):
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "avg"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)

        img = self.test_count.grayScaleMap
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        blur = cv2.GaussianBlur(img,(7,7),0)

        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,
                                    dp=1,
                                    minDist=self.test_params.minDist,
                                    param1=50,
                                    param2=self.test_params.sensitivity,
                                    minRadius=self.test_params.minRadius,
                                    maxRadius=self.test_params.maxRadius)
        circles = np.uint16(np.around(circles))

        circle_list = []
        for i in circles[0,:]:
            actual_color = self.test_count.getAverageColor(i)
            circle_list.append(actual_color)

        correct_color = True
        for i in range(len(beads)):
            calculated_color = beads[i][0]
            actual_color = circle_list[i][0]

            if(calculated_color != actual_color):
                correct_color = False

        self.assertTrue(correct_color)

    #FR. 6-3
    def test_middle_color_algorithm(self):
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)

        img = self.test_count.grayScaleMap
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        blur = cv2.GaussianBlur(img,(7,7),0)

        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,
                                    dp=1,
                                    minDist=self.test_params.minDist,
                                    param1=50,
                                    param2=self.test_params.sensitivity,
                                    minRadius=self.test_params.minRadius,
                                    maxRadius=self.test_params.maxRadius)
        circles = np.uint16(np.around(circles))

        circle_list = []
        for i in circles[0,:]:
            actual_color = self.test_count.getMiddleColor(i)
            circle_list.append(actual_color)

        correct_color = True
        for i in range(len(beads)):
            calculated_color = beads[i][0]
            actual_color = circle_list[i][0]

            if(calculated_color != actual_color):
                correct_color = False

        self.assertTrue(correct_color)

    #FR. 6-4
    def test_radius_color_algorithm(self):
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "rad"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)

        img = self.test_count.grayScaleMap
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        blur = cv2.GaussianBlur(img,(7,7),0)

        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,
                                    dp=1,
                                    minDist=self.test_params.minDist,
                                    param1=50,
                                    param2=self.test_params.sensitivity,
                                    minRadius=self.test_params.minRadius,
                                    maxRadius=self.test_params.maxRadius)
        circles = np.uint16(np.around(circles))

        circle_list = []
        for i in circles[0,:]:
            actual_color = self.test_count.getRadiusAverageColor(i)
            circle_list.append(actual_color)

        correct_color = True
        for i in range(len(beads)):
            calculated_color = beads[i][0]
            actual_color = circle_list[i][0]

            if(calculated_color != actual_color):
                correct_color = False

        self.assertTrue(correct_color)

    #FR. 6-5
    def test_four_corner_color_algorithm(self):
        self.test_params.maxRadius = 125
        self.test_params.minRadius = 0
        self.test_params.minDist = 20
        self.test_params.detectionAlgorithm = "corner"
        beads = self.test_count.getColorBeads(HoughConfig.DEFAULT, self.test_params)

        img = self.test_count.grayScaleMap
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        blur = cv2.GaussianBlur(img,(7,7),0)

        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,
                                    dp=1,
                                    minDist=self.test_params.minDist,
                                    param1=50,
                                    param2=self.test_params.sensitivity,
                                    minRadius=self.test_params.minRadius,
                                    maxRadius=self.test_params.maxRadius)
        circles = np.uint16(np.around(circles))

        circle_list = []
        for i in circles[0,:]:
            actual_color = self.test_count.getFourQuadrantColor(i)
            circle_list.append(actual_color)

        correct_color = True
        for i in range(len(beads)):
            calculated_color = beads[i][0]
            actual_color = circle_list[i][0]

            if(calculated_color != actual_color):
                correct_color = False

        self.assertTrue(correct_color)


class TestNonFunctionalRequirements(unittest.TestCase):

    #NFR. 1-1
    def test_stitching_accuracy(self):
        pass

    #NFR. 1-2
    def test_counting_accuracy(self):
        pass


if __name__ == '__main__':
    cov = coverage.Coverage(omit="./exp-env/*")
    cov.start()
    print('happening before', file=sys.stderr)
    unittest.main()
    print('happening after', file=sys.stderr)
    cov.stop()
    cov.save()
    cov.html_report()