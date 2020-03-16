import time
import sys

from datetime import datetime

try:
    import pandas as pd
except (ImportError, ModuleNotFoundError):
    print('\n', '\tpandas has not been imported.', '\n\n', '\texiting ...')
    sys.exit()
try:
    import numpy as np
except ModuleNotFoundError as error:
    print('\n', '\tnumpy has not been imported.', '\n\n', '\texiting ...')
    sys.exit()

import bikeshare_inputs as b_i
import bikeshare_constants as b_c


def show_data(df, city, month, day, row=0, increment=5):
    """
    Shows data for the specified city
    Args:
        (str) df - the data set
        (str) city - the city the user inputed
        (str) month - the month if inputed by the user
        (str) day - the day if inputed by the user
        (int) row - the row number on which to display the data
        (int) increment - how many rows to display
    """
    view = True
    # create a datafrane in order to show the row numbers of the filtered dataset
    #
    tmp = df.reset_index()

    stats = [{}]
    inputs = pd.DataFrame( stats, index = ['Inputs: '] )

    inputs['City'] = city.title()
    inputs['Month'] = month.title()
    inputs['Day'] = day.title()
    inputs['Number of Records'] = f'{len(df.index):,}'

    with pd.option_context(*b_c.PD_OPTIONS):
        print(inputs, '\n')

    # Show the first five records of the dataframe
    #
    beg_col, end_col, incre_col = 0, 5, 5
    print('\nFirst five records of the dataset\n')
    #
    # Get five fields at a time 
    #
    for col_idx in range( beg_col, len(b_c.COLUMN_HEADINGS), incre_col ):
        with pd.option_context(*b_c.PD_OPTIONS):
            #
            # print the five fields
            #
            print( tmp.loc[row:row+increment, b_c.COLUMN_HEADINGS[beg_col:end_col]], '\n')
            #
            # increment the beg and end fields by five
            #
            beg_col += incre_col
            end_col += incre_col

    # Show the first five records of the dataframe
    #
    print( '\nLast five records of the dataset\n')
    #
    # Get five fields at a time 
    #
    beg_col, end_col, incre_col = 0, 5, 5
    for col_idx in range( beg_col, len(b_c.COLUMN_HEADINGS), incre_col ):
        with pd.option_context(*b_c.PD_OPTIONS):
            #
            # print the five fields
            #
            print( tmp.loc[len(tmp)-5:,b_c.COLUMN_HEADINGS[beg_col:end_col]], '\n')
            #
            # increment the beg and end fields by five
            #
            beg_col += incre_col
            end_col += incre_col

    print()
    while view:
        # Ask the user if they want to see another five records of data
        #
        proceed = b_i.get_yes_or_no("View another 5 rows of data? ")
        if ( not proceed ):
            break
        row += 5
        #
        # Get five fields at a time 
        #
        beg_col, end_col, incre_col = 0, 5, 5
        for col_idx in range( beg_col, len(b_c.COLUMN_HEADINGS), incre_col ):
            with pd.option_context(*b_c.PD_OPTIONS):
                #
                # print the five fields
                #
                print( tmp.loc[row:row+increment,b_c.COLUMN_HEADINGS[beg_col:end_col]], '\n')
                #
                # increment the beg and end fields by five
                #
                beg_col += incre_col
                end_col += incre_col
        print()

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(b_c.CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    b_c.COLUMN_HEADINGS = sorted( list(df.columns), key=str.casefold)

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    #
    try:
        df['Day of Week'] = df['Start Time'].dt.weekday_name
    except AttributeError:
        df['Day of Week'] = df['Start Time'].dt.day_name()
    #
    df['Hour'] = df['Start Time'].dt.hour
    df['Year'] = df['Start Time'].dt.year
    #
    df['Trips'] = df['Start Station'] + '->' + df['End Station']
    #
    try:
        df['Year of Birth'] = df['Birth Year'].dropna().astype(int)
    except:
        print()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = list( b_c.MONTH_NAMES.values() )
        month = months.index(month.title()) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    b_c.clear_screen() # print a set of characters to clear the screen

    print('Bikeshare data has been loaded for the city: {}!\n\nLets proceed with the data analysis!\n'.format(city))

    return df

def main():

    #city, month, day = get_filters()
    print("Testing: load_data")
    df = load_data('chicago', 'all', 'all')

    print("Testing: show_data")
    show_data(df, 'chicago', 'all', 'all', row=0, increment=5)

if __name__ == "__main__":
    main()
