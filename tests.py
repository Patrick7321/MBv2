import unittest
import os
import csv
import colorsys
import cv2

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
        self.test_count = Counting('test/test_crushed_bead_directory/maps/result_default.jpg')
        self.test_params = Parameters()

    #FR. 2-1
    def test_single_crushed_bead(self):
        pass
    
    #FR. 2-2
    def test_no_crushed_beads(self):
        pass
        
    #FR. 2-3
    def test_multiple_crushed_bead(self):
        pass
        
    #FR. 2-4
    def test_crushed_bead_off_with_crushed(self):
        pass
        
    #FR. 2-5
    def test_crushed_bead_off_without_crushed(self):
        pass
        
    #FR. 2-6
    #Error - Video
    
    #FR. 2-7
    #Error - Video
    
    #FR. 2-8
    #Error - Video
    
    #FR. 2-9
    #Error - Video

    #FR. 2-10
    #Error - Video
    
    #FR. 2-11
    def test_cracked_beads_with_crushed(self):
        pass
        
    #FR. 2-12
    def test_cracked_beads_without_crushed(self):
        pass
        
    #FR. 2-13
    #Error - Video
    
    #FR. 2-14
    #Error - Video


class TestWaterBubble(unittest.TestCase):
    
    #FR. 3-1
    def test_water_bubble(self):
        pass
        
    #FR. 3-2
    def test_no_water_bubble(self):
        pass
    
    #FR. 3-3
    def test_multiple_water_bubbles(self):
        pass

    #FR. 3-4
    def test_water_bubble_off_with_bubble(self):
        pass
        
    #FR. 3-5
    def test_water_bubble_off_without_bubble(self):
        pass
        
    #FR. 3-6
    #Error - Video
    
    #FR. 3-7
    #Error - Video
    
    #FR. 3-8
    #Error - Video
    
    #FR. 3-9
    #Error - Video
    
    #FR. 3-10
    #Error - Video
    
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
        self.assertEqual(len(beads), 6)
        
    
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
    unittest.main()