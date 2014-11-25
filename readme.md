# PiMotion
===

Forked from Leo (DoctorWhoof) to make minor changes. Tweaked code a bit to suite my needs, and did some refactoring. Enjoy

###Changes:
===

 - Script now takes command line arguments, that overrides default values. Check the table below for list of arguments, descriptions and default values
 - It is possible now not to record (start script with `--recording false` argument)
 
 
### Argument table
===
#### Example script run: `python init.py --[argument] [value]` (without brackets)

| Argument      | Description | Default Value  |
| ------------- |:-------------:| -----:|
| `recording`   | Set this to `true` if you want recording to occur upon detecting motion | `false` |
| `dates`   | Set this to `true` if you want to use dates as folders, example: year/month/day/file | `false` |
| `width`   | Capture width | `640` |
| `height`   | Capture height | `480` |
| `bitrate`   | Capture bitrate | `0` |
| `quantization`   | Capture quantization, 10 is very high quality, 40 is very low. Use bitrate = 0 if quantization is non-zero. | `20` |
| `timerstart`   | Only allows recording after this hour | `0` |
| `timerstop`   | Only allows recording before this hour | `24` |
| `videoreduction` | A video recorded at 1920x1440 will be scaled by half and saved at 960x720, reducing noise. For best result, set this to `2` | `2` |
| `nightvideoreduction` | Scaling for nightMode | `2` |
| `mintail` | How long to keep testing for motion after last activity before committing file | `10` |
| `videofps` | Video file framerate | `15` |
| `rotation` | Image rotation, `warning: cropping will occur!` | `0` |
| `path` | Base videos path, defaults to init.py path | `pathof(init.py)` |
| `prefix` | Video file prefix | `""` |
| `tomp4` | Convert to MP4? Requires GPAC to be installed. Removes original .h264 file. If you want .mp4 files instead of .h264, install gpac with `sudo apt-get install -y gpac`| `false` |
| `preview` | Whether the preview window will be opened when running inside X. | `false` |
| `testinterval` | Interval at which stills are captured to test for motion | `0.25` |
| `testwidth` | Motion testing horizontal resolution. `Use low values!` | `96` |
| `testheight` | Motion testing vertical resolution. `Use low values!` | `72` |
| `threshold` | How much a pixel value has to change to consider it "motion". | `20` |
| `sensitivity` | How many pixels have to change to trigger motion detection. Good day values with no wind: 20 and 25; with wind: at least 30 and 50; good night values: 15 and 20? | `25` |



### Requirements
===
Requires installation of PIL and picamera modules:

`sudo apt-get install python-imaging-tk`

`sudo apt-get install python-picamera`