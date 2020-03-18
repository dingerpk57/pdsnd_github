# Constants
#
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_NAMES = { '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June' }


DAY_NAMES = { '0': 'Sunday', '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4': 'Thursday', '5': 'Friday', '6': 'Saturday' }

KEYBOARD_INTERRUPT_MSG = "Your special keystroke stopped this program and thus ended data analysis!"

ACTIONS = [ 'View raw data',
            'Analyze the time data',
            'Analyze the station data',
            'Analyze the trip duration data',
            'Analyze the users data',
            'Supply new inputs',
            'Exit' ]

INPUTS = [ "NO, please use strings 'all' as the filters for month and day.",
           "Filter by month",
           "Filter by day",
           "Filter by both day and month" ]


COLUMN_HEADINGS = []

MAX_COLWIDTH = 50
PD_OPTIONS = ('display.width', 132,
              'display.max_rows', None,
              'display.colheader_justify', 'center',
              'display.max_colwidth', MAX_COLWIDTH,
              'display.max_columns', None)

# Code to clear the screen when the screen is a vt100 terminal
def clear_screen():
  print(chr(27) + "[2J")

STATION_FIELDS = [ 'Start Station', 'End Station', 'Trips' ]
