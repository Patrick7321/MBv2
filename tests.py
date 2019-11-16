import unittest

from lib.counting import *
from Server.routes import *

class TestBeadSize(unittest.TestCase):


    def setUp(self):
        self.test_count = Counting('test/test_bead_size_directory/maps/result_default.jpg')
        self.test_params = Parameters()

    #FR. 1-1
    def test_beads_within_bounds(self):
        self.test_params.beadUpperBound = 125
        self.test_params.beadLowerBound = 0
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.OBJX10, self.test_params)
        self.assertEqual(len(beads), 4)

    #FR. 1-2
    def test_no_small_beads(self):
        self.test_params.beadUpperBound = 125
        self.test_params.beadLowerBound = 110
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.OBJX10, self.test_params)
        self.assertEqual(len(beads), 0)

    #FR. 1-3
    def test_no_big_beads(self):
        self.test_params.beadUpperBound = 80
        self.test_params.beadLowerBound = 20
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.OBJX10, self.test_params)
        self.assertEqual(len(beads), 0)
        
    #FR. 1-4
    def test_upper_bound_smaller_than_lower_bound(self):
        self.test_params.beadUpperBound = 50
        self.test_params.beadLowerBound = 80
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.OBJX10, self.test_params)
        #this should return an error
        
    #FR. 1-5
    def test_upper_bound_smaller_than_lower_default(self):
        self.test_params.beadUpperBound = 10
        self.test_params.beadLowerBound = 30
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.OBJX10, self.test_params)
        #this should return an error
        
    #FR. 1-6
    def test_lower_bound_larger_than_upper_default(self):
        self.test_params.beadUpperBound = 80
        self.test_params.beadLowerBound = 100
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.OBJX10, self.test_params)
        #this should return an error
        
    #FR. 1-7
    def test_default_size_bounds(self):
        self.test_params.beadUpperBound = 80;
        self.test_params.beadLowerBound = 30;
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.OBJX10, self.test_params)
        self.assertEqual(len(beads), 0)
        
    #FR. 1-8
    def test_upper_bound_equal_to_lower_bound(self):
        self.test_params.beadUpperBound = 40;
        self.test_params.beadLowerBound = 40;
        self.test_params.detectionAlgorithm = "mid"
        beads = self.test_count.getColorBeads(HoughConfig.OBJX10, self.test_params)
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
    #FR. 4-1
    def test_single_partial_bead(self):
        pass
    
    #FR. 4-2
    def test_no_partial_beads(self):
        pass

    #FR. 4-3
    def test_multiple_partial_bead(self):
        pass
    
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

    #FR. 5-1
    def test_csv_rows(self):
        pass

    #FR. 5-2
    def test_csv_type(self):
        pass
    
    #FR. 5-3
    def test_rgb_csv(self):
        pass
        
    #FR. 5-4
    def test_hsv_csv(self):
        pass
        
    #FR. 5-5
    def test_cymk_csv(self):
        pass
        
    #FR. 5-6
    def test_grayscale_csv(self):
        pass
        
    #FR. 5-7
    def test_invalid_stich(self):
        pass

class TestColorAlgorithms(unittest.TestCase):
        
    #FR. 6-1
    def test_default_color_algorithm(self):
        pass
        
    #FR. 6-2
    def test_average_color_algorithm(self):
        pass
        
    #FR. 6-3
    def test_middle_color_algorithm(self):
        pass
        
    #FR. 6-4
    def test_radius_color_algorithm(self):
        pass
       
    #FR. 6-5
    def test_four_corner_color_algorithm(self):
        pass


class TestNonFunctionalRequirements(unittest.TestCase):
        
    #NFR. 1-1
    def test_stitching_accuracy(self):
        pass
        
    #NFR. 1-2
    def test_counting_accuracy(self):
        pass
    
    
if __name__ == '__main__':
    unittest.main()