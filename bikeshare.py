import time
import sys

try:
    import pandas as pd
except ImportError as error:
    print('\n', '\tpandas has not been imported.', '\n\n', '\texiting ...')
    sys.exit()
try:
    import numpy as np
except ModuleNotFoundError as error:
    print('\n', '\tnumpy has not been imported.', '\n\n', '\texiting ...')
    sys.exit()

import bikeshare_constants as b_c
import bikeshare_inputs as b_i
import bikeshare_data as b_d
import bikeshare_stats as b_s

# Run the method which gets the user's inputs
#
city, month, day, proceed = b_i.get_inputs(df=None, city=None, month=None, day=None, proceed=True)
print()

# Load the data
#
df = b_d.load_data( city, month, day )

# Proceed with the analysis
#
while True:
    msg = "Do another analysis? "
    # Get the action (i.e Analyze the time data )
    set_action = b_i.get_action()
    if set_action == "View raw data":
        print()
        b_d.show_data(df, city, month, day, row=0, increment = 5 )
    elif set_action == "Analyze the time data":
        print()
        b_s.time_stats(df, city, month, day)
    elif set_action == "Analyze the station data":
        print()
        b_s.station_stats(df, city, month, day )
    elif set_action == "Analyze the trip duration data":
        print()
        b_s.trip_duration_stats(df, city, month, day )
    elif set_action == "Analyze the users data":
        print()
        b_s.user_stats(df, city, month, day )
    elif set_action == "Supply new inputs":
        print()
        city, month, day, proceed = b_i.get_inputs( None, None, None, None, False )
        df = b_d.load_data( city, month, day )
    else:
        # Stop
        #
        print()
        proceed = b_i.get_yes_or_no( "Are you sure? " )
        if proceed:
            break
   
print('\n', 'See ya!')
sys.exit()
