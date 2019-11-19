import coverage
from PIL import Image

from lib.counting import *
from lib.colorLabeler import *
from lib.file_util import *
from lib.stitching import *
from lib.util import *

from Server.routes import *

def main():
    cov = coverage.Coverage(omit=["./exp-env/*", "coverage_tests.py", './Server/*'])
    cov.start()

    test_single_upload()
    test_multiple_upload()
    test_directory_setup()
    test_invalid_stitch()

    cov.stop()
    cov.save()
    cov.html_report()

def test_single_upload():
    test_stitch = Stitching('test/coverage_test/single/images/', 'test/coverage_test/single/maps/')
    (test_status_id, test_status_string) = test_stitch.stitchImages_Default()
    test_count = Counting('test/test_bead_size_directory/maps/result_default.jpg')
    test_params = Parameters()
    test_params.maxRadius = 125
    test_params.minRadius = 0
    test_params.minDist = 20
    test_params.wantsCrushedBeads = True
    test_params.wantsWaterBubbles = True
    test_params.detectionAlgorithm = "mid"
    beads = test_count.getColorBeads(HoughConfig.DEFAULT, test_params)

def test_multiple_upload():
    test_stitch = Stitching('test/coverage_test/multiple/images/', 'test/coverage_test/multiple/maps/')
    (test_status_id, test_status_string) = test_stitch.stitchImages_Default()

    test_count = Counting('test/coverage_test/multiple/maps/result_default.jpg')
    test_params = Parameters()
    test_params.maxRadius = 125
    test_params.minRadius = 0
    test_params.minDist = 20
    test_params.detectionAlgorithm = "avg"
    test_params.wantsCrushedBeads = True
    test_params.wantsWaterBubbles = True
    beads1 = test_count.getColorBeads(HoughConfig.OBJX10, test_params)
    test_params.detectionAlgorithm = "rad"
    beads2 = test_count.getColorBeads(HoughConfig.OBJX4, test_params)
    test_params.detectionAlgorithm = "corner"
    beads3 = test_count.getColorBeads(HoughConfig.OBJX4, test_params)
    file_timestamp1 = test_count.makeBeadsCSV("hsv")
    file_timestamp2 = test_count.makeBeadsCSV("grayscale")
    file_timestamp3 = test_count.makeBeadsCSV("cmyk")
    file_timestamp4 = test_count.makeBeadsCSV("rgb")
    
def test_directory_setup():
    createUploadDir()
    filename1 = 'test/coverage_test/file_upload/test/test_image.jpg'
    image_file1 = Image.open(filename1)
    checkImagesAndSaveToDirectory([image_file1], 'test/coverage_test/file_upload')
    filename2 = 'test/coverage_test/file_upload/test/invalid_test_image.png'
    image_file2 = Image.open(filename2)
    checkImagesAndSaveToDirectory([image_file2], 'test/coverage_test/file_upload')

def test_invalid_stitch():
    test_stitch = Stitching('test/coverage_test/invalid_stitch/images/', 'test/coverage_test/invalid_stitch/maps/')
    (test_status_id, test_status_string) = test_stitch.stitchImages_Default()

main()