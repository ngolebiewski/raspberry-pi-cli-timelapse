#!/usr/bin/env python3
from picamera2 import Picamera2, Preview
import time
import os
import subprocess
from datetime import datetime
import random
from sys import argv

# SEE .env FILE FOR CLI COMMANDS TO CONNECT TO RASPBERRY PI and SCP FILES

def check_args():
    # expect 3 args: duration in S, interval in Seconds, boolean to run ffmpeg to convert to video
    duration, interval, to_video = 600, 10, False
    if len(argv) >= 2:
        try:
            duration = int(argv[1])
        except ValueError:
            print(f"Duration -- the 2nd arg '{argv[1]}' -- is not a number! The default of 600 seconds will be used.")
    if len(argv) >= 3:
        try:
            interval = int(argv[2])
        except ValueError:
            print(f"Interval -- the 3rd arg '{argv[2]}' -- is not a number! The default of 10 seconds will be used.")
    if len(argv) >= 4:
        if argv[3].lower() in ["true", "t", "1"]:
            to_video = True
        elif argv[3].lower() in ["false", "f", "0"]:
            to_video = False
        else:
            print(f"The 4th arg '{argv[3]}' should be a boolean and specifies whether or not you want ffmpeg to run and convert the images to a video file, defaulting to FALSE")
    return duration, interval, to_video
	

#Get the current datetime for filenaming
def get_datetime():
	now = datetime.now()
	formatted_time = now.strftime("%m%d%y-%I%M%p")
	return formatted_time

def take_timelapse(duration=600, interval=10, formatted_time=None):
    # total Duration  of the timelapse in seconds
    # Interval between captures in seconds
    
    if formatted_time is None:
        formatted_time = get_datetime()
    
    # Set up the directory to save images
    image_folder = f"timelapse_images/timelapse_images_{formatted_time}"
    os.makedirs(image_folder, exist_ok=True)

    # Initialize the camera
    picam2 = Picamera2()

    # Configure the camera for preview (you can adjust the configuration if needed)
    # camera_config = picam2.create_preview_configuration()
    
    camera_config = picam2.create_still_configuration(main={"size": (2592, 1944)})
    picam2.configure(camera_config)

    # Start the camera
    # picam2.start_preview(Preview.DRM)  # Use Preview.DRM for non-GUI environments
    picam2.start()

    # Delay
    delay = 10
    print(f"Delaying for {delay} seconds.")
    for i in range(delay):
        print("\033[34m.", end="")
        time.sleep(1)
    print("\n\033[0mDelay finished, starting recording.")
    
    # Capture images
    for i in range(0, duration, interval):
        image_filename = os.path.join(image_folder, f"img_{i//interval:05d}.jpg")
        picam2.capture_file(image_filename)
        print(f"Captured: {image_filename}")
        time.sleep(interval)

    # Stop the camera and preview
    picam2.stop_preview()
    picam2.stop()

    print("Timelapse capture complete.")
    return image_folder, formatted_time

def convert_to_video(image_folder, formatted_time):
    os.makedirs("timelapse_videos", exist_ok=True)
    # Define the output video filename
    output_video = f"timelapse_videos/timelapse_{formatted_time}.mp4"
    print(f"Output video will be saved as: {output_video}")

    # Check if ffmpeg is installed
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: FFmpeg is not installed. Please install FFmpeg to convert images to video.")
        return
    except subprocess.CalledProcessError as e:
        print(f"Error checking FFmpeg version: {e}")
        return

    # Define the ffmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-framerate', '24',  # Frames per second
        '-i', os.path.join(image_folder, 'img_%05d.jpg'),  # Image sequence pattern
        '-c:v', 'libx264',  # Video codec
        '-pix_fmt', 'yuv420p',  # Pixel format for better compatibility
        '-crf', '24',  # Constant rate factor for higher quality (lower is better quality)
        '-preset', 'slow',  # Use 'slow' or 'veryslow' for better compression (optional)
        # '-vf', 'scale=640:360',  # Adjust this to your desired resolution (e.g., 1920x1080)
        '-vf', 'scale=1280:720',  # Adjust this to your desired resolution (e.g., 1920x1080)
        output_video
    ]

    # Run the FFmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Timelapse video created: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the video: {e}")


def main():
    duration, interval, to_video = check_args()
    print(f"Duration: {duration}, Interval: {interval}, Convert to Video: {to_video}")
    current_time = get_datetime()
    print(f"Current Date Time: {current_time}")
    image_folder, formatted_time = take_timelapse(duration, interval, current_time)
    if to_video == True:
        convert_to_video(image_folder, formatted_time)


if __name__ == "__main__":
    main()