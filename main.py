import sys
import time
from arguments_parser import ArgumentsParser
from pimotion import Motion
from datetime import datetime


def main():
    # Parse arguments
    arg_parser = ArgumentsParser()

    # Get options from ArgumentsParser
    settings = arg_parser.options

    # Instantiate pimotion.py with arguments and/or default options
    motion = Motion(settings)

    print "\nMotionPi started with settings:"
    print settings

    print "Camera warm up..."
    time.sleep(2)
    print "Camera is active. Ctrl+C to terminate."

    try:
        while True:
            timenow = datetime.now()
            if timenow.hour >= motion.timerStart and timenow.hour <= motion.timerStop:
                if motion.usePreviewWindow:
                    motion.camera.start_preview()
                if motion.test_motion():
                    print 'Motion detected'
                    if settings.recording:
                        motion.start_recording()
                else:
                    if motion.timeWithoutActivity > motion.minimumTail:
                        # print "Motion stopped " + repr(motion.timeWithoutActivity) + " ago"
                        if settings.recording:
                            motion.stop_recording()
            time.sleep(motion.testInterval)
            motion.skip = False
    except KeyboardInterrupt:
        print "\nTerminating..."
        if motion.isRecording:
            motion.camera.stop_recording()
        motion.camera.stop_preview()
        motion.camera.close()
        sys.exit(1)
