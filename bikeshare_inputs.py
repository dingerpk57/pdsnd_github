import sys

try:
    from bullet import Bullet, YesNo, VerticalPrompt, SlidePrompt
    from bullet import colors
except ModuleNotFoundError as error:
    print('\n', '\tbullet has not been imported.', '\n\n', '\texiting ...')
    sys.exit()

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
import bikeshare_stats as b_s
import bikeshare_data as b_d

def get_action():
    """
    Asks user to specify an action to initiate.

    Returns:
        (str) action
    """
    actions = Bullet(
            prompt = "\nPlease choose an action: ",
            choices = list(action for action in b_c.ACTIONS), # Google#1
            indent = 0,
            align = 5,
            margin = 2,
            shift = 1,
            bullet = "*",
            pad_right = 5
        )

    try:
        action = actions.launch()

    except KeyboardInterrupt:
        print( "{}".format(b_c.KEYBOARD_INTERRUPT_MSG))
        sys.exit()

    return action

def get_city():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) city - name of the city to analyze
    """
    cities = Bullet(
            prompt = "\nPlease choose a city [move cursor with arrow keys]",
            choices = list(city.title() for city in b_c.CITY_DATA.keys()), # Google#1
            indent = 0,
            align = 5,
            margin = 2,
            shift = 1,
            bullet = "*",
            pad_right = 5
        )

    try:
        city = cities.launch()

    except KeyboardInterrupt:
        print( "{}".format(b_c.KEYBOARD_INTERRUPT_MSG))
        sys.exit()

    return city.lower()

def get_month():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    months = Bullet(
            prompt = "\nPlease choose the month (only through june): ",
            choices = list( b_c.MONTH_NAMES.values() ),
            indent = 0,
            align = 5,
            margin = 2,
            shift = 1,
            bullet = "*",
            pad_right = 5
            )
    
    try:
        month = months.launch()

    except KeyboardInterrupt:
        print( "{}".format(b_c.KEYBOARD_INTERRUPT_MSG))
        sys.exit()

    return month.lower()

def get_day():
    """
    Asks user to specify a day to analyze.

    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    days_of_week = Bullet(
            prompt = "\nPlease choose the day of the week: ",
            choices = list( b_c.DAY_NAMES.values() ),
            indent = 0,
            align = 5,
            margin = 2,
            shift = 1,
            bullet = "*",
            pad_right = 5
            )

    try:
        day = days_of_week.launch()

    except KeyboardInterrupt:
        print( "{}".format(b_c.KEYBOARD_INTERRUPT_MSG))
        sys.exit()

    return day.lower()

def get_time_filter():
    """
    Asks user to specify how to filter the data if at all.

    Returns:
        (str) time_filter
    """
    time_filter = Bullet(
        prompt = "\nWould you like to filter the data?",
        choices = list(action for action in b_c.INPUTS), # Google#1
        # choices = ["NO, please use strings 'all' as the filters for month and day.", "Filter by month", "Filter by day", "Filter by both day and month"],
        indent = 0,
        align = 5,
        margin = 2,
        shift = 1,
        bullet = "*",
        pad_right = 5
        )

    try:
        time_filter = time_filter.launch()

    except KeyboardInterrupt:
        print( "{}".format(b_c.KEYBOARD_INTERRUPT_MSG))
        sys.exit()

    return time_filter

def get_yes_or_no( prompt_str ):
    """
    Asks the user for a yes or no response.
    Args:
        (str) prompt_str - the question

    Returns:
        (boolean) yes (true) or no (false)
    """
    is_yes_or_no = VerticalPrompt(
            [
              YesNo("{}".format(prompt_str)
                    )
              ],
              spacing = 1
            )

    try:
        yes_or_no = is_yes_or_no.launch()[0][1]

    except:
        print( "{}".format("Bad keystroke - try again"))
        yes_or_no = get_yes_or_no( prompt_str )

    return yes_or_no

def get_inputs( df, city, month, day, proceed ):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    b_c.clear_screen() # print a set of characters to clear the screen

    if proceed:
        print('Hello! Let\'s explore some US bikeshare data!')

    # Get the user's input for the city
    #
    city = get_city()

    # Get the user's time filter and process accordingly
    #
    if month is None and day is None:
        #
        answer = get_time_filter()
        #
        if answer == "Filter by both day and month":
            month = get_month()
            day = get_day()
        elif answer == "Filter by month":
            month = get_month()
            day = "all"
        elif answer == "Filter by day":
            month = "all"
            day = get_day()
        else:
            month = "all"
            day = "all"

    print( '\nInput complete.\n\nNow data is being loaded ...\n' )

    proceed = True

    return city, month, day, proceed

def show_inputs( df,  city, month, day ):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (dataframe)) df - a pandas object which stores the bikestare data
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """
    # Make variables to store the inputs and the summary
    #
    inputs = [{'City': city.title(), 'Month': month.title(), 'Day of Week': day}]
    summary = pd.DataFrame( inputs, index = ['Your inputs:']) 

    # Count and store the number of records in the dataframe
    #
    if df is not None:
        summary['Number of Records'] = f'{len(df.index):,}'
        # Get the column headings (not used)
        #
        # summary['Field Names'] = ''
        # ix = 1
        # for field_name in sorted( list(df.columns), key=str.casefold ):
        #    summary.loc[ ix, 'Field Names'] = field_name.ljust( 20, ' ' )
        #    ix += 1

        # summary = summary.fillna('')

    with pd.option_context(*b_c.PD_OPTIONS):
        print( summary ) # google -> python pandas print indent dataframes

def main():
    
    print("Testing: get_action") 
    get_action()

    print("\nTesting: get_city") 
    get_city()

    print("\nTesting: get_time_filter")
    get_time_filter()
        
    print("\nTesting: get_month") 
    get_month()
        
    print("\nTesting: get_day") 
    get_day()

    print("\nTesting: get_inputs")
    df, city, month, day, proceed = None, None, None, None, True
    city, month, day, proceed = get_inputs( df, city, month, day, proceed )
    
    print("\nTesting: show_inputs")
    show_inputs( df,  city, month, day )

    print("\nTesting: get_yes_or_no")
    get_yes_or_no( "Testing complete?")

if __name__ == "__main__":
    main()
