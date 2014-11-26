import os
import optparse


class ArgumentsParser:
    def __init__(self):
        # Instantiate optparse
        self.parser = optparse.OptionParser()

        # Setup parse arguments and get results
        self.options = self.setup_parser()

    def setup_parser(self):
        # Should we record on motion detection
        self.parser.add_option('--recording', action="store", dest="recording", default=False)

        # Should we use dates as folders, example: year/month/day/file
        self.parser.add_option('--dates', action="store", dest="dates", default=False)

        # Resolution width
        self.parser.add_option('--width', action="store", dest="width", default=640, type='int')

        # Resolution height
        self.parser.add_option('--height', action="store", dest="height", default=480, type='int')

        # Bit rate
        self.parser.add_option('--bitrate', action="store", dest="bit_rate", default=0, type='int')

        # Quantization
        self.parser.add_option('--quantization', action="store", dest="quantization", default=20, type='int')

        # Timer start
        self.parser.add_option('--timerstart', action="store", dest="timer_start", default=0, type='int')

        # Timer stop
        self.parser.add_option('--timerstop', action="store", dest="timer_stop", default=24, type='int')

        # Video reduction
        self.parser.add_option('--videoreduction', action="store", dest="video_reduction", default=2, type='int')

        # Night video reduction
        self.parser.add_option('--nightvideoreduction', action="store", dest="night_video_reduction", default=2, type='int')

        # Minimum tail
        self.parser.add_option('--mintail', action="store", dest="min_tail", default=10.0, type='float')

        # Video file framerate.
        self.parser.add_option('--videofps', action="store", dest="video_fps", default=15, type='int')

        # Image rotation
        self.parser.add_option('--rotation', action="store", dest="rotation", default=0, type='int')

        # Base videos path, defaults to init.py path (if !set)
        current_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        self.parser.add_option('--path', action="store", dest="path", default=current_path, type="string")

        # File prefix
        self.parser.add_option('--prefix', action="store", dest="prefix", default="", type="string")

        # Convert to MP4?
        self.parser.add_option('--tomp4', action="store", dest="convert_to_mp4", default=False)

        # Preview window (X)
        self.parser.add_option('--preview', action="store", dest="preview", default=False)

        # Test interval
        self.parser.add_option('--testinterval', action="store", dest="test_interval", default=0.25, type="float")

        # Test width
        self.parser.add_option('--testwidth', action="store", dest="test_width", default=96, type="int")

        # Test height
        self.parser.add_option('--testheight', action="store", dest="test_height", default=72, type="int")

        # Threshold
        self.parser.add_option('--threshold', action="store", dest="threshold", default=20, type="int")

        # Sensitivity
        self.parser.add_option('--sensitivity', action="store", dest="sensitivity", default=25, type="int")

        # Parse arguments
        (options, args) = self.parser.parse_args()

        return options