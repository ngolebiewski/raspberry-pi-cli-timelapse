import requests
import json
import sys
from datetime import datetime
import subprocess

def get_sunsets():
    base_url = 'https://api.sunrisesunset.io/'
    lat_long='lat=40.71427&lng=-74.00597'
    start_date = '2024-11-14'
    end_date = '2024-11-15'
    # https://api.sunrisesunset.io/json?lat=40.71427&lng=-74.00597
    # &date_start=1990-05-01&date_end=1990-07-01
    
    response = requests.get(f'{base_url}json?{lat_long}&date_start={start_date}&date_end={end_date}&time_format=24')
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
        sun_data = response.json()['results']
        return sun_data
    else:
        print("Failed to fetch sunrise and sunset data from server")
        sys.exit(1)
    
    """
    returns list of objects with the following...
        {
      "date": "2024-11-18",
      "sunset": "4:37:58 PM",
      "first_light": "5:11:54 AM",
      "last_light": "6:13:08 PM",
      "dawn": "6:17:34 AM",
      "dusk": "5:07:28 PM",
      "solar_noon": "11:42:31 AM",
      "golden_hour": "3:57:01 PM",
      "day_length": "9:50:52",
      "timezone": "America/New_York",
      "utc_offset": -300
    },
    """
    
    
def set_sunsets(sun_data):
    pass

def strip_seconds(time_with_secs):
    # time_with_secs like "06:42:21" and returns "06:42"
    formatted_time = datetime.strptime(time_with_secs, "%H:%M:%S").strftime("%H:%M")
    return formatted_time

def format_date(date_old):
    # 2024-11-15 to 11-15-2024
    date_obj = datetime.strptime(date_old, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%m/%d/%Y")
    return formatted_date
    
def parse_sun_info(sun_data):
    sun_tuples = []
    for sunstats in sun_data:
        date = format_date(sunstats['date'])
        dawn = strip_seconds(sunstats['dawn'])
        golden_hour = strip_seconds(sunstats['golden_hour'])
        print("date:", date, "dawn:", dawn, "golden_hour:", golden_hour)
        sun_tuples.append(tuple((date, dawn, golden_hour)))
        print("sun_tuples: ", sun_tuples)
    return sun_tuples

def create_at_commands(sun_tuples):
    at_commands = []
    dir = '/home/calderg/Documents/coding_projects/raspberry-pi-cli-timelapse'
    python_loc = '/usr/bin/python'
    script = 'timelapse_3.py 3600 20 True'
    log = f'/home/calderg/Documents/coding_projects/raspberry-pi-cli-timelapse/timelapse_sun_setter.log 2>&1'
    for times in sun_tuples:
        at_dawn = f'echo "cd {dir} && {python_loc} {script} >> {log}" | at {times[1]} {times[0]}'
        at_golden_hour = f'echo "cd {dir} && {python_loc} {script} >> {log}" | at {times[2]} {times[0]}'
        # print(at_dawn)
        # print(at_golden_hour)
        at_commands.append(at_dawn)
        at_commands.append(at_golden_hour)
    # print(at_commands)
    return at_commands

        
        
        
    # {
    #   "date": "2024-11-15",
    #   "sunrise": "06:43:32",
    #   "sunset": "16:40:20",
    #   "first_light": "05:08:52",
    #   "last_light": "18:15:01",
    #   "dawn": "06:14:14",
    #   "dusk": "17:09:39",
    #   "solar_noon": "11:41:56",
    #   "golden_hour": "15:59:48",
    #   "day_length": "9:56:48",
    #   "timezone": "America/New_York",
    #   "utc_offset": -300
    # }                

def write_at_jobs(at_commands, on=False):
    if on:
        print('writing jobs')
        for command in at_commands:
            try:
                subprocess.run(command, shell=True, check=True)
                print(f"Successfully scheduled: {command}")
            except subprocess.CalledProcessError as e:
                print(f"Error scheduling command: {command} - {e}")
    else:
        print('not writing jobs')

def main():
    sun_data = get_sunsets()
    sun_tuples = parse_sun_info(sun_data)
    at_commands = create_at_commands(sun_tuples)
    write_at_jobs(at_commands, on=True)

if __name__=="__main__":
    main()
    
'''
Steps to Use at on a Raspberry Pi

sudo apt install at
sudo systemctl start atd
sudo systemctl enable atd  # To start at boot

'''