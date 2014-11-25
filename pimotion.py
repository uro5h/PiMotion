# Script created by Leo Santos ( http://www.leosantos.com )
# Tweaked a bit by uro5h ( www.github.com/uro5h )
# Based on the picam.py script (by brainflakes, pageauc, peewee2 and Kesthal) and picamera examples.

import picamera
import cStringIO
import subprocess
from datetime import datetime

from PIL import Image


class Motion:
    def __init__(self, settings):
        # To achieve 30 fps, set this to 1920x1080 or less (cropping will occur)
        # Set this to a high resolution. The video file will be scaled down using "width" and "height" to reduce noise.
        self.captureWidth = settings.width

        # Setting these to more than 1920x1440 seems to cause slowdown (records at a lower frame rate)
        self.captureHeight = settings.height

        # default is 17000000
        self.bitrate = settings.bit_rate

        # 10 is very high quality, 40 is very low. Use bitrate = 0 if quantization is non-zero.
        self.quantization = settings.quantization

        # only allows recording after this hour
        self.timerStart = settings.timer_start

        # only allows recording before this hour
        self.timerStop = settings.timer_stop

        # For best results set this to 2.
        # A video recorded at 1920x1440 will be scaled by half and saved at 960x720, reducing noise.
        self.videoReduction = settings.video_reduction

        # scaling for nightMode.
        self.nightVideoReduction = settings.night_video_reduction

        # If True, light sensitivity is increased at the expense of image quality
        self.allowNightMode = False

        # how long to keep testing for motion after last activity before committing file
        self.minimumTail = settings.min_tail

        # Video file frame rate.
        self.framerate = settings.video_fps

        # Rotates image (warning: cropping will occur!)
        self.rotation = settings.rotation

        # Local file path for video files
        self.filepath = settings.path

        # Optional filename prefix
        self.prefix = settings.prefix

        # Requires GPAC to be installed. Removes original .h264 file
        # If you want .mp4 files instead of .h264, install gpac with "sudo apt-get install -y gpac" and set convertToMp4=True
        self.convertToMp4 = settings.convert_to_mp4

        # Creates folders with current year, month and day, then saves file in the day folder.
        self.useDateAsFolders = settings.dates

        # Whether the preview window will be opened when running inside X.
        self.usePreviewWindow = settings.preview

        # Interval at which stills are captured to test for motion
        self.testInterval = settings.test_interval

        # motion testing horizontal resolution. Use low values!
        self.testWidth = settings.test_width

        # motion testing vertical resolution. Use low values!
        self.testHeight = settings.test_height

        # TODO: make command line arguments from this settings
        self.testStart = [0, 24]  # coordinates to start testing for motion
        self.testEnd = [80, 71]  # coordinates to finish testing for motion

        # How much a pixel value has to change to consider it "motion"
        self.threshold = settings.threshold

        # How many pixels have to change to trigger motion detection
        # Good day values with no wind: 20 and 25; with wind: at least 30 and 50; good night values: 15 and 20?
        self.sensitivity = settings.sensitivity

        # The camera object
        self.camera = picamera.PiCamera()

        # How long since last motion detection
        self.timeWithoutActivity = 0.0

        # How long since last frame without motion detected
        self.lastTimeWithoutActivity = datetime.now()

        # The time at which the last motion detection occurred
        self.lastStartedRecording = 0.0

        # Is the camera currently recording? Prevents stopping a camera that is not recording.
        self.isRecording = False

        # Skips the first frame, to prevent a false positive motion detection (since the first image1 is black)
        self.skip = True

        self.nightMode = False
        self.filename = ""
        self.mp4name = ""
        self.folderPath = ""

        # initializes image1
        self.image1 = Image.new('RGB', (self.testWidth, self.testHeight))

        # initializes image2
        self.image2 = Image.new('RGB', (self.testWidth, self.testHeight))

        # initializes image1 "raw data" buffer
        self.buffer1 = self.image1.load()

        # The difference here is that image1 is handled like a file stream,
        # while the buffer is the actual RGB byte data, if I understand it correctly!

        # initializes image2 "raw data" buffer
        self.buffer2 = self.image2.load()

        self.camera.resolution = ( self.captureWidth, self.captureHeight )
        self.camera.framerate = self.framerate
        self.camera.rotation = self.rotation

        # Values are: average, spot, matrix, backlit
        self.camera.meter_mode = "average"

        # Instantiate variables for later
        self.width = 0
        self.height = 0

    def start_recording(self):
        if not self.isRecording and not self.skip:
            timenow = datetime.now()

            if self.useDateAsFolders:
                self.folderPath = self.filepath + "%04d/%02d/%02d" % ( timenow.year, timenow.month, timenow.day )
                subprocess.call(["mkdir", "-p", self.folderPath])
                self.filename = self.folderPath + "/" + self.prefix + "%02d-%02d-%02d.h264" % (
                    timenow.hour, timenow.minute, timenow.second )
            else:
                self.filename = self.filepath + self.prefix + "%04d%02d%02d-%02d%02d%02d.h264" % (
                    timenow.year, timenow.month, timenow.day, timenow.hour, timenow.minute, timenow.second )

            if (( timenow.hour >= 20 ) or ( timenow.hour <= 5 )) and ( self.allowNightMode == True ):
                self.camera.exposure_mode = "night"
                self.camera.image_effect = "denoise"
                self.camera.exposure_compensation = 25
                self.camera.ISO = 800
                self.camera.brightness = 70
                self.camera.contrast = 50
                self.width = int(self.captureWidth / self.nightVideoReduction)
                self.height = int(self.captureHeight / self.nightVideoReduction)
                self.nightMode = True
            else:
                self.camera.exposure_mode = "auto"
                self.camera.image_effect = "none"
                self.camera.exposure_compensation = 0
                self.camera.ISO = 0
                self.camera.brightness = 50
                self.camera.contrast = 0
                self.width = int(self.captureWidth / self.videoReduction)
                self.height = int(self.captureHeight / self.videoReduction)
                self.nightMode = False

            self.mp4name = self.filename[:-4] + "mp4"
            self.camera.start_recording(self.filename, resize=(self.width, self.height), quantization=self.quantization,
                                        bitrate=self.bitrate)
            self.isRecording = True
            print "Started recording %s" % self.filename + " with night mode = " + str(self.nightMode)

    def stop_recording(self):
        if self.isRecording:
            self.camera.stop_recording()
            self.isRecording = False
            self.skip = True
            if self.convertToMp4:
                subprocess.call(["MP4Box", "-fps", str(self.framerate), "-add", self.filename, self.mp4name])
                subprocess.call(["rm", self.filename])
                print "\n"
            else:
                print "Finished recording."

    def capture_test_image(self):
        self.camera.image_effect = "none"
        self.image1 = self.image2
        self.buffer1 = self.buffer2
        image_data = cStringIO.StringIO()
        self.camera.capture(image_data, 'bmp', use_video_port=True, resize=(self.testWidth, self.testHeight))
        image_data.seek(0)
        im = Image.open(image_data)
        image_buffer = im.load()
        image_data.close()
        return im, image_buffer

    def test_motion(self):
        changed_pixels = 0
        self.image2, self.buffer2 = self.capture_test_image()
        for x in xrange(self.testStart[0], self.testEnd[0]):
            for y in xrange(self.testStart[1], self.testEnd[1]):
                pixdiff = abs(self.buffer1[x, y][1] - self.buffer2[x, y][1])
                if pixdiff > self.threshold:
                    changed_pixels += 1
        if changed_pixels > self.sensitivity:
            self.timeWithoutActivity = 0
            self.lastTimeWithoutActivity = datetime.now()
            return True
        else:
            self.timeWithoutActivity += ( datetime.now() - self.lastTimeWithoutActivity ).total_seconds()
            self.lastTimeWithoutActivity = datetime.now()
            return False