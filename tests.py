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
    
    #FR. 4-1
    #Error - Colorless Bead
    
    #FR. 4-2
    #Error - Colorless Bead
    
    #FR. 4-3
    #Error - Colorless Bead
    
    #FR. 4-4
    #Error - Colorless Bead
    
    #FR. 4-5
    #Error - Colorless Bead
    
    #FR. 4-6
    #Error - Colorless Bead
    
    #FR. 4-7
    #Error - Colorless Bead
    
    #FR. 4-8
    #Error - Colorless Bead
    
    #FR. 4-9
    #Error - Colorless Bead
    
    #FR. 4-10
    #Error - Colorless Bead
    
    #FR. 4-11
    #Error - Colorless Bead
    
    #FR. 4-12
    #Error - Colorless Bead


class TestCSV(unittest.TestCase):
    
    #FR. 5-1
    def test_rgb_csv(self):
        pass
        
    #FR. 5-2
    def test_hsv_csv(self):
        pass
        
    #FR. 5-3
    def test_cymk_csv(self):
        pass
        
    #FR. 5-4
    def test_grayscale_csv(self):
        pass
        
    #FR. 5-5
    def test_invalid_stich(self):
        pass
        
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
        
    #NFR. 1-1
    def test_stitching_accuracy(self):
        pass
        
    #NFR. 1-2
    def test_counting_accuracy(self):
        pass
    
    
if __name__ == '__main__':
    unittest.main()