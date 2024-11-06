# Timelapse Camera for Raspberry Pi Zero
## Intended to run upon booting the device, no GUI/interaction

APT INSTALLS on RASPBERRY PI
1. picamera2 
2. ffmpeg

** Need a camera installed! **

Takes 3 args when you run it:
`python timelapse_3.py 600 10 False`

those are the defaults as well. Feel free to run as `python timelapse_3.py`
- 600 = duration in seconds 
- - 10 = interval between photos in seconds
False/True = to be processed by ffmpeg into a video. False is a good option for pi Zero because it's too much processing and the machine spins out.

1. Set up a crontab -e and add this line: `TBD` <- Really, I will have this soon!>
2. Note, `killall python` if you ssh in to your device and want to stop the script from running.

You can view the timelapse video here: [Timelapse Video](media/timelapse_102824-0228PM.mp4)

