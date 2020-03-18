import time
import sys
import re
from datetime import datetime

# The following tests if the pandas and numpy libraries have been loaded
#
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

import bikeshare_inputs as b_i
import bikeshare_constants as b_c
import bikeshare_data as b_d

def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    # Set up variables in order to store the statistics
    #
    stats = [{}]
    inputs = pd.DataFrame(stats, index = ['Inputs: '])

    # Set up a variable to store the inputs which will later be printed
    #
    inputs['City'] = city.title()
    inputs['Month'] = month.title()
    inputs['Day'] = day.title()
    inputs['Number of Records'] = f'{len(df.index):,}'

    # Show the user inputs
    #
    with pd.option_context(*b_c.PD_OPTIONS):
        print(inputs, '\n')

    # Define a variable to store the results
    #
    results = pd.DataFrame( stats, index = ['Mode: ', 'Count: '] )

    # Get the mode and convert to 12 hour AM/PM
    #
    mode_start_hour = str(df['Hour'].mode()[0])
    mode_start_hour = datetime.strptime(mode_start_hour, "%H").strftime("%I %p")
    results['Trip Start hour'] = datetime.strptime(str( df['Hour'].mode()[0] ), "%H").strftime("%I %p")
    # Count the number of trips for that hour
    #
    results['Trip Start hour']['Count: '] = f'{list(df["Hour"].value_counts())[0]:,}'

    with pd.option_context(*b_c.PD_OPTIONS):
        print(results, '\n')

    if month == 'all':
        # Print a title
        #
        title_month = 'Trip Start hour (by Month)'
        print(' '*12, title_month.center(50,' '), '\n', ' '*11, ('-'*(len(title_month))).center(50, ' '))

        results_month = pd.DataFrame( columns = list(b_c.MONTH_NAMES.values()), index = ['Mode: ', 'Count: '] )

        # Get the mode for the trip start hour by month
        #
        for m, hours in df.groupby('Month')['Hour']:
            # Convert the 24 hour value to 12 hour with the right AM/PM
            #
            mode_start_hour = str(list(hours.mode())[0])
            mode_start_hour = datetime.strptime(mode_start_hour, "%H").strftime("%I %p")
            results_month[b_c.MONTH_NAMES[str(m)]]['Mode: '] = mode_start_hour
            # Report the count for that trip start hour
            #
            results_month[b_c.MONTH_NAMES[str(m)]]['Count: '] = f'{list(hours.value_counts())[0]:,}'

        with pd.option_context(*b_c.PD_OPTIONS):
            print(results_month, '\n')

    if day == 'all':
        # Print a title
        #
        title_day = 'Trip Start hour (by Day)'
        print(' '*12, title_day.center(50,' '), '\n', ' '*11, ('-'*(len(title_day))).center(50, ' '))
        
        results_day = pd.DataFrame( columns = list(b_c.DAY_NAMES.values()), index = ['Mode: ', 'Count: '] )

        # Get the mode for the trip start hour by day
        #
        for d, hours in df.groupby('Day of Week')['Hour']:
            # Convert the trip start hour into 12 hour AM/PM format
            #
            mode_start_hour = str(list(hours.mode())[0])
            mode_start_hour = datetime.strptime(mode_start_hour, "%H").strftime("%I %p")
            results_day[d]['Mode: '] = mode_start_hour
            # Report the count for that trip start hour
            #
            results_day[d]['Count: '] =  f'{list(hours.value_counts())[0]:,}'

        with pd.option_context(*b_c.PD_OPTIONS):
            print(results_day, '\n')

    b_i.get_yes_or_no( "Pause. " )
    b_c.clear_screen()


def station_stats(df, city, month, day ):
    """Displays statistics on the most popular stations and trip."""

    # Set up variables in order to store the inputs
    #
    stats = [{}]

    inputs = pd.DataFrame( stats, index = ['Inputs: '] )
    
    # Set up a variable to store the inputs which will later be printed
    #
    inputs['City'] = city.title()
    inputs['Month'] = month.title()
    inputs['Day of Week'] = day.title()
    inputs['Number of Records'] = f'{len(df.index):,}'

    with pd.option_context(*b_c.PD_OPTIONS):
        print(inputs, '\n')

    title_month = 'Station Stats'
    print(' '*12, title_month.center(50,' '), '\n', ' '*11, ('-'*(len(title_month))).center(50, ' '))

    results = pd.DataFrame( stats, index = ['Mode: ', 'Count: ', 'Range: '] )

    # Collect the mode of the start station,
    # plus why it is the mode (count).
    # Finally, report how many unique start stations there were (range)
    #
    results['Start Station'] = df['Start Station'].mode()[0]
    results['Start Station']['Count: '] = f'{list(df["Start Station"].value_counts())[0]:,}'
    results['Start Station']['Range: '] = f'{len(df["Start Station"].value_counts()):,}'

    # Collect the mode of the end station,
    # plus why it is the mode (count).
    # Finally, report how many unique end stations there were (range)
    #
    results['End Station'] = df['End Station'].mode()[0]
    results['End Station']['Count: '] = f'{list(df["End Station"].value_counts())[0]:,}'
    results['End Station']['Range: '] = f'{len(df["End Station"].value_counts()):,}'

    # Collect the mode of the trip,
    # plus why it is the mode (count).
    # Finally, report how many unique trips there were (range)
    #
    results['Trips'] = df['Trips'].mode()[0]
    results['Trips']['Count: '] = f'{list(df["Trips"].value_counts())[0]:,}'
    results['Trips']['Range: '] = f'{len(df["Trips"].value_counts()):,}'

    with pd.option_context(*b_c.PD_OPTIONS):
        print(results, '\n')

    print('\nLegend: Trips show Start Station and End Station separated by \'->\'.',
          '\n        Count shows how many trips there were for that mode.',
          '\n        Range shows how many total unique trips there were.\n')

    b_i.get_yes_or_no( "Pause. " )
    b_c.clear_screen()

    if month == 'all':
        # Print a title
        #
        title_month = 'Station Stats (by Month)'
        print(' '*12, title_month.center(50,' '), '\n',
              ' '*11, ('-'*(len(title_month))).center(50, ' '))

        results_month = pd.DataFrame( columns = list(b_c.MONTH_NAMES.values()),
                                      index = ['Station Stats'] )

        # Loop through the months
        #
        for m in list(b_c.MONTH_NAMES.keys()):
            #
            results = pd.DataFrame( stats, index = ['Mode: ', 'Count: ', 'Range: '] )
            #
            for field_name in 'Start Station', 'End Station', 'Trips':
                #
                # get mode, count, range of the three fields
                #
                mode_f_n = df[df['Month'] == int(m)][field_name].mode()[0]
                count_f_n = f'{list(df[df["Month"] == int(m)][field_name].value_counts())[0]:,}'
                range_f_n = f'{len(df[df["Month"] == int(m)][field_name].value_counts()):,}'
                #
                # store the mode, count, range of each field
                #
                results[field_name] = mode_f_n
                results[field_name]['Count: '] = count_f_n
                results[field_name]['Range: '] = range_f_n

            
            print(' '*12, b_c.MONTH_NAMES[str(m)].center(50,' '), '\n',
                  ' '*11, ('-'*(len(b_c.MONTH_NAMES[str(m)]))).center(50, ' '))
            with pd.option_context(*b_c.PD_OPTIONS):
                print(results, '\n')

        print('\nLegend: Trips show Start Station and End Station separated by \'->\'.',
              '\n        Count shows how many trips there were for that mode.',
              '\n        Range shows how many total unique trips there were.\n')

        b_i.get_yes_or_no( "Pause. " )
        b_c.clear_screen()

    if day == 'all':
        # Print a title
        #
        title_month = 'Station Stats (by Day)'
        print(' '*12, title_month.center(50,' '), '\n',
              ' '*11, ('-'*(len(title_month))).center(50, ' '))

        results_month = pd.DataFrame( columns = list(b_c.MONTH_NAMES.values()),
                                      index = ['Station Stats'] )

        # Loop through the months
        #
        for d in list(b_c.DAY_NAMES.values()):
            #
            results = pd.DataFrame( stats, index = ['Mode: ', 'Count: ', 'Range: '] )
            #
            for field_name in 'Start Station', 'End Station', 'Trips':
                #
                # get mode, count, range of the three fields
                #
                mode_f_n = df[df['Day of Week'] == d][field_name].mode()[0]
                count_f_n = f'{list(df[df["Day of Week"] == d][field_name].value_counts())[0]:,}'
                range_f_n = f'{len(df[df["Day of Week"] == d][field_name].value_counts()):,}'
                #
                # store the mode, count, range of each field
                #
                results[field_name] = mode_f_n
                results[field_name]['Count: '] = count_f_n
                results[field_name]['Range: '] = range_f_n
            
            print(' '*12, d.center(50,' '), '\n', ' '*11, ('-'*(len(d))).center(50, ' '))
            with pd.option_context(*b_c.PD_OPTIONS):
                print(results, '\n')

        print('\nLegend: Trips show Start Station and End Station separated by \'->\'.',
              '\n        Count shows how many trips there were for that mode.',
              '\n        Range shows how many total unique trips there were.\n')

        b_i.get_yes_or_no( "Pause. " )
        b_c.clear_screen()


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    # Set up variables in order to store the inputs
    #
    stats = [{}]
    inputs = pd.DataFrame( stats, index = ['Inputs: '] )

    # Set up a variable to store the inputs which will later be printed
    #
    inputs['City'] = city.title()
    inputs['Month'] = month.title()
    inputs['Day of Week'] = day.title()
    inputs['Number of Records'] = f'{len(df.index):,}'

    with pd.option_context(*b_c.PD_OPTIONS):
        print(inputs, '\n')

    results = pd.DataFrame( stats, index = ['Sum: ', 'Mean: '] )

    # Calculate in minutes the total travel time
    # 
    minutes = f'{int(df["Trip Duration"].sum() // 60):,}' + ' minutes '
    seconds = str(int(df["Trip Duration"].sum() % 60)) + ' Seconds'
    #
    results['Trip Duration'] = minutes + seconds

    # Calculate the mean travel time
    #
    mean_trip_duration = "{0:.2f}".format(df["Trip Duration"].mean() / 60)
    results['Trip Duration']['Mean: '] = mean_trip_duration + ' Minutes'

    with pd.option_context(*b_c.PD_OPTIONS):
        print('\n', results, '\n')

    if month == 'all':
        # Calculate in minutes the total travel time and the average but by month
        #
        results_month = pd.DataFrame( columns = list(b_c.MONTH_NAMES.values()),
                                      index = ['Sum: ', 'Mean: '] )

        title_month = 'Trip Duration (by Month)'
        print(' '*12, title_month.center(50,' '), '\n', ' '*11, ('-'*(len(title_month))).center(50, ' '))

        for m, durations in df.groupby('Month')['Trip Duration']:
            # Calculate the sum and then convert to minutes and secs,
            # and format the minutes into thousands
            #
            minutes = f'{int(durations.sum() // 60):,}' + ' minutes '
            seconds = str(int(durations.sum() % 60)) + ' Seconds'
            results_month[b_c.MONTH_NAMES[str(m)]]['Sum: '] = minutes + seconds
            #
            # Calculate the mean but format it with two decimal places
            #
            mean_trip_duration = "{0:.2f}".format(durations.mean() / 60) + ' Minutes'
            results_month[b_c.MONTH_NAMES[str(m)]]['Mean: '] = mean_trip_duration

        with pd.option_context(*b_c.PD_OPTIONS):
            print(results_month, '\n')

    if day == 'all':
        # Calculate in minutes the total travel time and the average but by day
        #
        results_day = pd.DataFrame( columns = list(b_c.DAY_NAMES.values()),
                                    index = ['Sum: ', 'Mean: '] )

        title_day = 'Trip Duration (by Day)'
        print(' '*12, title_day.center(50,' '), '\n', ' '*11, ('-'*(len(title_day))).center(50, ' '))

        for d, durations in df.groupby('Day of Week')['Trip Duration']:
            # Calculate the sum and then convert to minutes and secs,
            # and format the minutes into thousands
            #
            minutes = f'{int(durations.sum() // 60):,}' + ' minutes '
            seconds = str(int(durations.sum() % 60)) + ' Seconds'
            results_day[d]['Sum: '] = minutes + seconds
            #
            # Calculate the mean but format it with two decimal places
            #
            mean_trip_duration = "{0:.2f}".format(durations.mean() / 60) + ' Minutes'
            results_day[d]['Mean: '] = mean_trip_duration

        with pd.option_context(*b_c.PD_OPTIONS):
            print(results_day, '\n')

    b_i.get_yes_or_no( "Pause. " )
    b_c.clear_screen()


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    # Set up variables in order to store the inputs
    #
    stats = [{}]
    inputs = pd.DataFrame( stats, index = ['Inputs: '] )
    
    # Set up a variable to store the inputs which will later be printed
    #
    inputs['City'] = city.title()
    inputs['Month'] = month.title()
    inputs['Day of Week'] = day.title()
    inputs['Number of Records'] = f'{len(df.index):,}'

    with pd.option_context(*b_c.PD_OPTIONS):
        print(inputs, '\n')

    results = pd.DataFrame( stats, index = ['Count: ', 'Percentage: '] )

    # Count the number of trips by user type
    #
    prt_str = ''
    for user_type, count in df['User Type'].agg(lambda x: x.value_counts().to_dict()).items():
        # Combine the user type and the count into a string
        # in order to combine the user types as a single value
        #
        prt_str += ('[' + user_type[0] + ']:').ljust(7) + f'{count:,}'.rjust(7) + ' '
        results['Trips by User Type'] = prt_str
    
    # Convert the count of number of trips into percentage by user type
    #
    # https://blog.softhints.com/pandas-count-percentage-value-column/
    #
    prt_str = ''
    user_type = df['User Type']
    items_u_t = user_type.agg(lambda x: (x.value_counts(normalize=True)
                                          .mul(100)
                                          .round(1)
                                          .astype(str) + '%')
                                          .to_dict()).items()
    for user_type, percent in items_u_t:
        #
        # Combine the user type and the percentage into a string in order to make a single value
        #
        prt_str += ('[' + user_type[0] + ']:').ljust(7) + percent.rjust(7) + ' '
        results['Trips by User Type']['Percentage: '] = prt_str

    with pd.option_context(*b_c.PD_OPTIONS):
        print('\n', results, '\n')
    
    if month == 'all':
        # Calculate the count and percentage of user type by month
        #
        results_month = pd.DataFrame( columns = list(b_c.MONTH_NAMES.values()),
                                      index = ['Count: ', 'Percentage: '] )

        title_month = 'Trips by User Type (by Month)'
        print(' '*12, title_month.center(50,' '), '\n',
              ' '*11, ('-'*(len(title_month))).center(50, ' '))

        # Get the counts of user types by month
        #
        prt_str = ''
        month_u_t = df.groupby('Month')['User Type']
        dict_items = dict(month_u_t.agg(lambda x: x.value_counts().to_dict())).items()
        for m, counts in dict_items:
            #
            # loop through each month's counts
            #
            for user_type, count in list(counts.items()):
                # Combine the user type and the count into a string in order to make a single value
                #
                prt_str += ('[' + user_type[0] + ']:').ljust(7) + f'{count:,}'.rjust(7) + ' '

            results_month[b_c.MONTH_NAMES[str(m)]] = prt_str + '|'
            prt_str = ''

        # Calculate the percentages of user types by month
        #
        month_u_t = df.groupby('Month')['User Type']
        dict_items = dict(month_u_t.agg(lambda x: (x.value_counts(normalize=True)
                                                    .mul(100)
                                                    .round(1)
                                                    .astype(str) + '%')
                                                    .to_dict())).items()
        for m, percentages in dict_items:
            # loop through each month's percentages
            #
            for user_type, percent in list(percentages.items()):
                # Combine the user type and the percentages into a string in order to make single value
                #
                prt_str += ('[' + user_type[0] + ']:').ljust(7) + percent.rjust(7) + ' '

            results_month[b_c.MONTH_NAMES[str(m)]]['Percentage: '] = prt_str + '|'
            prt_str = ''

        with pd.option_context(*b_c.PD_OPTIONS):
            print(results_month, '\n')
    
    if day == 'all':
        # Calculate the count and percentage of user type by day
        #
        results_day = pd.DataFrame( columns = list(b_c.DAY_NAMES.values()),
                                    index = ['Count: ', 'Percentage: '] )

        title_day = 'Trips by User Type (by Day)'
        print(' '*12, title_day.center(50,' '), '\n',
              ' '*11, ('-'*(len(title_day))).center(50, ' '))

        # Get the counts of user types by day
        #
        prt_str = ''
        day_u_t = df.groupby('Day of Week')['User Type']
        dict_items = dict(day_u_t.agg(lambda x: x.value_counts().to_dict())).items()
        for d, counts in dict_items:                                                     
            # loop through each day's counts
            #
            for user_type, count in list(counts.items()):
                # Combine the user type and the count into a string in order to make a single value
                #
                prt_str += ('[' + user_type[0] + ']:').ljust(7) + f'{count:,}'.rjust(7) + ' '
            
            results_day[d] = prt_str + '|'
            prt_str = ''

        # Calculate the percentages of user types by day
        #
        day_u_t = df.groupby('Day of Week')['User Type']
        dict_items = dict(day_u_t.agg(lambda x: (x.value_counts(normalize=True)
                                                  .mul(100)
                                                  .round(1)
                                                  .astype(str) + '%')
                                                  .to_dict())).items()
        for d, percentages in dict_items:
            # loop through each day's percentages
            #
            for user_type, percent in list(percentages.items()):
                # Combine the user type and the percentages into a string in order to make a single value
                #
                prt_str += ('[' + user_type[0] + ']:').ljust(7) + percent.rjust(7) + ' '

            results_day[d]['Percentage: '] = prt_str + '|'
            prt_str = ''

        with pd.option_context(*b_c.PD_OPTIONS):
            print(results_day, '\n')

    print('\nLegend: [S] -> Subscriber.', '\n        [C] -> Customer.\n        [D] -> Dependent.\n')

    b_i.get_yes_or_no( "Pause. " )
    b_c.clear_screen()

    with pd.option_context(*b_c.PD_OPTIONS):
        print('\n', inputs, '\n')

    # Count the number of trips by gender of the rider and also include that count as a percentage
    #
    # Define an error if the data field Gender was not included in the dataset
    #
    try:        
        stats = [{}]
        results = pd.DataFrame( stats, index = ['Count: ', 'Percentage: '] )

        # Count the number of trips by gender
        #
        prt_str = ''
        for gender, count in df['Gender'].agg(lambda x: x.value_counts().to_dict()).items():
            # Combine the gender and count into a string in order to make a single value
            #
            prt_str += (gender + ':').ljust(7) + f'{count:,}'.rjust(7) + ' '
            results['Trips by Gender'] = prt_str
        
        # Calculate the percentage of bike trips by gender
        #
        prt_str = ''
        gender_items = df['Gender'].agg(lambda x: (x.value_counts(normalize=True)
                                                    .mul(100)
                                                    .round(1)
                                                    .astype(str) + '%')
                                                    .to_dict()).items()
        for gender, percent in gender_items:
            # Combine the gender and the percentage into a string in order to make a single value
            #
            prt_str += (gender + ':').ljust(7) + percent.rjust(7) + ' '
            results['Trips by Gender']['Percentage: '] = prt_str

        with pd.option_context(*b_c.PD_OPTIONS):
            print('\n', results, '\n')
        
        if month == 'all':
            # Count the number of bike trips by gender and by month
            # and also calculate the percentage
            #
            results_month = pd.DataFrame( columns = list(b_c.MONTH_NAMES.values()),
                                          index = ['Count: ', 'Percentage: '] )

            title_month = 'Trips by Gender (by Month)'
            print(' '*12, title_month.center(50,' '), '\n',
                  ' '*11, ('-'*(len(title_month))).center(50, ' '))

            # Loop through each month getting the counts
            #
            prt_str = ''
            dict_items = dict(df.groupby('Month')['Gender'].agg(lambda x: x.value_counts()
                                                                           .to_dict())).items()
            for m, counts in dict_items:
                #
                # Loop through each gender getting its percent
                #
                for gender, count in list(counts.items()):
                    #
                    # Combine the gender and the counts into a string
                    # in order to make a single value
                    #
                    prt_str += (gender + ':').ljust(7) + f'{count:,}'.rjust(7) + ' '
               
                results_month[b_c.MONTH_NAMES[str(m)]] = prt_str + '|'
                prt_str = ''

            # Loop through each month getting the percentages
            #
            month_g = df.groupby('Month')['Gender']
            dict_items = dict(month_g.agg(lambda x: (x.value_counts(normalize=True)
                                                      .mul(100)
                                                      .round(1)
                                                      .astype(str) + '%')
                                                      .to_dict())).items()
            for m, percentages in dict_items:
                #
                # Loop through each gender getting its percent
                #
                for gender, percent in list(percentages.items()):
                    #
                    # Combine the gender and the percentages into a string
                    # in order to make a single value
                    #
                    prt_str += (gender + ':').ljust(7) + percent.rjust(7) + ' '
                
                results_month[b_c.MONTH_NAMES[str(m)]]['Percentage: '] = prt_str + '|'
                prt_str = ''

            with pd.option_context(*b_c.PD_OPTIONS):
                print(results_month, '\n')
      
        if day == 'all':
            # Count the number of bike trips by gender and by day
            # and also calculate the percentage
            #
            results_day = pd.DataFrame( columns = list(b_c.DAY_NAMES.values()),
                                        index = ['Count: ', 'Percentage: '] )

            title_day = 'Trips by Gender (by Day)'
            print(' '*12, title_day.center(50,' '), '\n',
                  ' '*11, ('-'*(len(title_day))).center(50, ' '))

            # Loop through each day getting the counts
            #
            prt_str = ''
            day_g = df.groupby('Day of Week')['Gender']
            dict_items = dict(day_g.agg(lambda x: x.value_counts()
                                                   .to_dict())).items()
            for d, counts in dict_items:
                #
                # Loop through each gender getting its count
                #
                for gender, count in list(counts.items()):
                    #
                    # Combine the gender and the counts into a string
                    # in order to make a single value
                    #
                    prt_str += (gender + ':').ljust(7) + f'{count:,}'.rjust(7) + ' '
                
                results_day[d] = prt_str + '|'
                prt_str = ''

            # Loop through each day getting the percentages
            #
            day_g = df.groupby('Day of Week')['Gender']
            dict_items = dict(day_g.agg(lambda x: (x.value_counts(normalize=True)
                                                    .mul(100)
                                                    .round(1)
                                                    .astype(str) + '%')
                                                    .to_dict())).items()
            for d, percentages in dict_items:
                #
                # Loop through each gender getting its percent
                #
                for gender, percent in list(percentages.items()):
                    #
                    # Combine the gender and the percentages into a string
                    # in order to make a single value
                    #
                    prt_str += (gender + ':').ljust(7) + percent.rjust(7) + ' '
               
                results_day[d]['Percentage: '] = prt_str + '|'
                prt_str = ''

            with pd.option_context(*b_c.PD_OPTIONS):
                print(results_day, '\n')

    except:
        print('No data collected for the gender of the bike rider.\n')

    b_i.get_yes_or_no( "Pause. " )
    b_c.clear_screen()

    with pd.option_context(*b_c.PD_OPTIONS):
        print('\n', inputs, '\n')

    # Display earliest, most recent, and most common year of birth
    #
    stats = [{}]
    results = pd.DataFrame( stats, index = ['Max: ', 'Min: ', 'Mode: '] )

    try:
        # Find the max value for the birth year (youngest bike rider)
        #
        results['Rider Birth Year'] = str(int(df['Year of Birth'].max()))

        # Find the min value for the birth year (youngest bike rider)
        #
        results['Rider Birth Year']['Min: '] = str(int(df['Year of Birth'].min()))

        # Find the mode value for the birth year (most common birth year of the rider)
        #
        results['Rider Birth Year']['Mode: '] =df['Year of Birth'].mode()[0] 

        with pd.option_context(*b_c.PD_OPTIONS):
            print('\n', results, '\n')

        if month == 'all':
            # Find the max, min, mode of the bike rider's birth year by month
            #
            results_month = pd.DataFrame( columns = list(b_c.MONTH_NAMES.values()),
                                          index = ['Max: ', 'Min: ', 'Mode: '] )

            title_month = 'Rider Birth Year (by Month)'
            print(' '*12, title_month.center(50,' '), '\n',
                  ' '*11, ('-'*(len(title_month))).center(50, ' '))

            # Loop through each month
            #
            for m, birth_year in df.groupby('Month')['Year of Birth']:
                #
                # Find the max, min, mode of the birth year
                #
                month_name = b_c.MONTH_NAMES[str(m)]
                results_month[month_name] = str(int(birth_year.max()))
                results_month[month_name]['Min: '] = str(int(birth_year.min()))
                results_month[month_name]['Mode: '] = str(int(birth_year.mode()[0]))

            with pd.option_context(*b_c.PD_OPTIONS):
                print(results_month, '\n')

        if day == 'all':
            # Find the max, min, mode of the bike rider's birth year by day
            #
            results_day = pd.DataFrame( columns = list(b_c.DAY_NAMES.values()),
                                        index = ['Max: ', 'Min: ', 'Mode: '] )

            title_day = 'Rider Birth Year (by Day)'
            print(' '*12, title_day.center(50,' '), '\n',
                  ' '*11, ('-'*(len(title_day))).center(50, ' '))

            for day_name, birth_year in df.groupby('Day of Week')['Year of Birth']:
                #
                # Find the max, min, mode of the birth year
                #
                results_day[day_name] = str(int(birth_year.max()))
                results_day[day_name]['Min: '] = str(int(birth_year.min()))
                results_day[day_name]['Mode: '] = str(int(birth_year.mode()[0]))

            with pd.option_context(*b_c.PD_OPTIONS):
                print(results_day)

        print('\nLegend: Max means youngest.', '\n        Min means oldest.\n')

    except:
        print('No data collected on the birth year of the rider.\n')

    b_i.get_yes_or_no( "Pause. " )
    b_c.clear_screen()


def main():
    while True:
        #city, month, day = get_filters()
        print("Start testing: load data")
        df = load_data('chicago', 'all', 'all')
        break

        #time_stats(df)
        #station_stats(df)
        #trip_duration_stats(df)
        #user_stats(df)

        #restart = input('\nWould you like to restart? Enter yes or no.\n')
        #if restart.lower() != 'yes':
        #    break


if __name__ == "__main__":
	main()
