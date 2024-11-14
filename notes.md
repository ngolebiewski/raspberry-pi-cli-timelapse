### Let's say you want to get the amount of time between first light and sunrise...then add on a 1/2 hour...

from datetime import datetime

# Define two datetime objects
datetime1 = datetime(2024, 11, 14, 12, 30, 0)
datetime2 = datetime(2024, 11, 14, 14, 45, 0)

# Calculate the difference between the two
time_difference = datetime2 - datetime1

# Get the number of seconds
seconds = time_difference.total_seconds()

print(f"The number of seconds between the two datetime objects is: {seconds}")

OR...

# Create datetime objects from strings
datetime1 = datetime.strptime("2024-11-14 08:30", "%Y-%m-%d %H:%M")
datetime2 = datetime.strptime("2024-11-14 14:45", "%Y-%m-%d %H:%M")

# Calculate the difference
time_difference = datetime2 - datetime1

# Get the number of seconds
seconds = time_difference.total_seconds()

print(f"The number of seconds between the two datetime objects is: {seconds}")