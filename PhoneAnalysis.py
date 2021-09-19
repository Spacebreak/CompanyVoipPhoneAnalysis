import csv
import logging
# import pprint

from datetime import date

# Try to open a file in read mode. If unsuccessful the method handles the error and tries again.
def open_file():
    file_opened = False

    # Gets user input for file name. Attempts to open the file and returns it.
    while not file_opened:
        try:
            local_file_name = input('What is the name of the file you want to try and open? \n')
            file_data = open(f'C:\\Shane\\Files\\Work\\Payslips and Tax\\GenBiome\\{local_file_name}.csv', 'r')
            file_opened = True
            return file_data
        except IOError as ex:
            logging.info(f"Caught exception opening a file with the users input of {local_file_name}.".format(ex))
            print(f"Could not find a file with the name of {local_file_name}.csv")

    # Ensures to close the file if it is open.
    if file_data.open():
        file_data.close()


# Convert American formatted date into normal date format. Splits the date and returns the string reorganized.
def convert_american_date_format(american_date_to_convert):
    split_date = american_date_to_convert.split('/')
    converted_date = split_date[1] + '/' + split_date[0] + '/' + split_date[2]
    return converted_date


# Convert a date in the format DD/MM/YYYY to a day of the week (e.g. Monday) using datetime module.
def convert_date_to_day(date_to_convert):
    date_split = date_to_convert.split('/')
    calendar_day = date(int(date_split[2]), int(date_split[1]), int(date_split[0])).strftime('%A')
    return calendar_day


# Takes a dictionary for the day of the week, and total the calls for each day, then get the average.
def calculate_average_calls_per_day(day_of_week):
    day_total_calls = 0

    for key, value in day_of_week.items():
        day_total_calls += value

    day_average_calls = day_total_calls / len(day_of_week)

    # To get the name of the day again I generate a list of keys from a dictionary and feed it back into the Conversion
    # method that takes a date and calculates which day of the week this falls onto.
    print(f'The average calls received on a {convert_date_to_day(list(day_of_week.keys())[0])} '
          f'are: {day_average_calls}')

    return day_average_calls


# Create dictionary reader object from an open file
file_name = open_file()
file_to_be_read = csv.DictReader(file_name)

# From the dictionary reader object, extract each line into a list of call records
list_of_call_records = []
for line in file_to_be_read:
    list_of_call_records.append(line)

# A dictionary saving unique dates a call was received along with how many calls received on that day.
# Dictionaries don't allow duplicates - desired.
unique_dates = {}

# From the list of call records, extract the field called 'Start Time' and split the time from the date
for x in range(len(list_of_call_records)):
    date_extract = list_of_call_records[x]['Start Time'].split(" ")[0]  # 0 element captures first split element only.

    legible_date = convert_american_date_format(date_extract)

    # Check if the date is in the dictionary, if it is - increase it's value by 1. This signifies that another call has
    # occurred on this date. If not in the dictionary it will be added with the value of 1.
    if legible_date in unique_dates:
        unique_dates[legible_date] += 1
    else:
        unique_dates[legible_date] = 1

    # print(list_of_call_records[x]['Start Time'])

print(f"The following dates had calls to the office: {unique_dates}")

# Initialize dictionaries for each day of the week. We are going to use the datetime module to check what day of the
# week a date is. This will allow us to compare trends for specific days e.g if Thursdays are busier than Mondays.
mondays = {}
tuesdays = {}
wednesdays = {}
thursdays = {}
fridays = {}
saturdays = {}
sundays = {}

# For each value in the unique dates dictionary, convert this to a calendar day and add it to the correct dictionary.
for key, value in unique_dates.items():
    print(f'On {key}, you had {value} phone calls to the clinic.')

    day_of_the_week = convert_date_to_day(key)

    if day_of_the_week == "Monday":
        mondays[key] = value
    elif day_of_the_week == "Tuesday":
        tuesdays[key] = value
    elif day_of_the_week == "Wednesday":
        wednesdays[key] = value
    elif day_of_the_week == "Thursday":
        thursdays[key] = value
    elif day_of_the_week == "Friday":
        fridays[key] = value
    elif day_of_the_week == "Saturday":
        saturdays[key] = value
    elif day_of_the_week == "Sunday":
        sundays[key] = value

# Add every day to a dictionary that correlates the day of the week to the value of days.
allDays = {'Mondays' : mondays, 'Tuesdays' : tuesdays, 'Wednesdays' : wednesdays, 'Thursdays' : thursdays,
           'Fridays' : fridays, 'Saturdays' : saturdays, 'Sundays' : sundays}

# Iterate through each value inside of each dictionary of days stored in allDays.
for day in allDays:
    print(f'Results for {day} are: {allDays.get(day)}')

# Calculate the average calls received on each day of the week. Will compare all mondays to each other.
averageMonday = calculate_average_calls_per_day(mondays)
averageTuesday = calculate_average_calls_per_day(tuesdays)
averageWednesday = calculate_average_calls_per_day(wednesdays)
averageThursday = calculate_average_calls_per_day(thursdays)
averageFriday = calculate_average_calls_per_day(fridays)
averageSaturday = calculate_average_calls_per_day(saturdays)
averageSunday = calculate_average_calls_per_day(sundays)