import datetime
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# calculates time data for month and day
def calculate_time_data(df, column, time_dict):
    time_series = df[column].value_counts(sort=True)
    time_int = time_series.first_valid_index()
    time_name = str(time_dict[time_int])
    time_events = time_series[time_series.first_valid_index()]
    return time_name, time_events


# calculates hour, station, and birth year data
def calculate_name_events_data(df, column):
    entity_series = df[column].value_counts(sort=True)
    entity_name = entity_series.first_valid_index()
    entity_events = entity_series[entity_series.first_valid_index()]
    return entity_name, entity_events


# calculates user data for type and gender
def calculate_user_data(df, column):
    user_series = df[column].value_counts(sort=True)
    user_tuples = user_series.iteritems()
    return user_tuples


# asks user to specify a city, month, and day to analyze
def get_filters():
    """
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # define allowable city, month, and day lists
    city_list = ['chicago', 'new york city', 'washington']
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    day_list = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    print('\n\nHello! Let\'s explore some U.S. bikeshare data!\n')

    # filter on city
    while True:
        city = str(input('Which city\'s data would you like to investigate? Chicago, New York City, or Washington?\n')).lower()
        if city in city_list:
            break
        else:
            print('Please input a correct city option.\n')
            continue

    # filter on month
    while True:
        month = str(input('\nHow would you like to filter by month? All, January, ...December?\n')).lower()
        if month in month_list:
            break
        else:
            print('Please input a correct month option.\n')
            continue

    # filter on day
    while True:
        day = str(input('\nHow would you like to filter by day? All, Monday, ...Sunday?\n')).lower()
        if day in day_list:
            break
        else:
            print('Please input a correct day option.\n')
            continue

    # display filters
    print('\nLet\'s filter data for {} by month: {} and day: {}!'.format(city.title(), month.title(), day.title()))
    print('\n' + ('-'*70))
    return city, month, day


# loads data for the specified city and filters by month and day if applicable
def load_data(CITY_DATA, city, month, day):
    """
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # set up month and day numeric conversions for check against converted time
    month_numeric = { 'all': 0,
                      'january': 1,
                      'february': 2,
                      'march': 3,
                      'april': 4,
                      'may': 5,
                      'june': 6,
                      'july': 7,
                      'august': 8,
                      'september': 9,
                      'october': 10,
                      'november': 11,
                      'december': 12 }
    day_numeric = { 'monday': 0,
                    'tuesday': 1,
                    'wednesday': 2,
                    'thursday': 3,
                    'friday': 4,
                    'saturday': 5,
                    'sunday': 6 }

    # read csv data for city as pandas dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert dataframe start time column to datetime object and create new columns for month and day of the week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.dayofweek
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter dataframe by month and day filters
    if month != 'all':
        df = df[df['Month'] == month_numeric[month]]
    if day != 'all':
        df = df[df['Day of Week'] == day_numeric[day]]

    return df


# displays statistics on the most frequent times of travel
def time_stats(df, month, day, city):
    month_name = { 1: 'january',
                      2: 'february',
                      3: 'march',
                      4: 'april',
                      5: 'may',
                      6: 'june',
                      7: 'july',
                      8: 'august',
                      9: 'september',
                      10: 'october',
                      11: 'november',
                      12: 'december' }
    day_name = { 0: 'monday',
                 1: 'tuesday',
                 2: 'wednesday',
                 3: 'thursday',
                 4: 'friday',
                 5: 'saturday',
                 6: 'sunday' }

    print('\nCalculating The Most Frequent Times of Travel... [Frame 1 of 4]\n')
    start_time = time.time()

    # calculate the most common month given no month filter ie. month filter of 'all'
    most_common_month_name, number_month_events = calculate_time_data(df, 'Month', month_name)

    # calculate the most common day of week
    most_common_day_name, number_day_events = calculate_time_data(df, 'Day of Week', day_name)

    # calculate the most common start hour
    most_common_start_hour_int, number_start_hour_events = calculate_name_events_data(df, 'Start Hour')

    # print calculation messages
    # print month and day data
    if month != 'all' and day != 'all':
        print('\nThere were {} events on {}s for the month of {} in {}.'.format(number_day_events, day.title(), month.title(), city.title()))
    else:
        if month == 'all':
            print('\nThe most common month for {} was {}, with {} events.'.format(city.title(), most_common_month_name.title(), number_month_events))
        else:
            print('\n{} had {} events in {}.'.format(city.title(), number_month_events, month.title()))
        if day == 'all':
            print('\nThe most common day for {} was {}, with {} events.'.format(city.title(), most_common_day_name.title(), number_day_events))
        else:
            print('\n{} had {} events on {}s.'.format(city.title(), number_day_events, day.title()))
    # print event data
    print('\nThe most common start time hour was {}, with {} events.\n'.format(most_common_start_hour_int, number_start_hour_events))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n' + ('-'*70))


# displays statistics on the most popular stations and trip
def station_stats(df):
    print(('-'*70) + '\n\nCalculating The Most Popular Stations and Trip... [Frame 2 of 4]\n')
    start_time = time.time()

    # calculate most commonly used start station
    most_common_start_station, most_common_start_station_events = calculate_name_events_data(df, 'Start Station')

    # calculate most commonly used end station
    most_common_end_station, most_common_end_station_events = calculate_name_events_data(df, 'End Station')

    # calculate most frequent combination of start station and end station trip
    df['Trips'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_trips_name, most_common_trips_events = calculate_name_events_data(df, 'Trips')

    # print calculation messages
    # print start station
    print('\nThe most common start station is: {}, with {} instances.'.format(most_common_start_station.title(), most_common_start_station_events))
    # print end station
    print('\nThe most common end station is: {}, with {} instances.'.format(most_common_end_station.title(), most_common_end_station_events))
    # print trip
    print('\nThe most common trip was from {}, with {} instances.\n'.format(most_common_trips_name.title(), most_common_trips_events))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n' + ('-'*70))


# displays statistics on the total and average trip duration
def trip_duration_stats(df):
    print(('-'*70) + '\n\nCalculating Trip Duration... [Frame 3 of 4]\n')
    start_time = time.time()

    # calculate total travel time
    total_travel_time = int(sum(df['Trip Duration']))

    # calculate mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())

    # print calculation messages
    # print total time
    print('\nTotal travel time is {} seconds.'.format(total_travel_time))
    # print mean time
    print('\nMean travel time is {} seconds.\n'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n' + ('-'*70))


# displays statistics on bikeshare users
def user_stats(df):
    print(('-'*70) + '\n\nCalculating User Stats... [Frame 4 of 4]\n')
    start_time = time.time()

    # calculate counts of user types
    user_types_tuples = calculate_user_data(df, 'User Type')

    # calculate counts of gender
    user_gender_tuples = calculate_user_data(df, 'Gender')

    # calculate birth year data, remove 'nan' values, convert to int, sort list
    df = df.dropna(subset=['Birth Year'])
    most_common_birth_year_list = list(df['Birth Year'])
    most_common_birth_year_list.sort()
    # calculate most recent and earliest birth years
    most_recent_birth_year = int(most_common_birth_year_list[-1])
    most_early_birth_year = int(most_common_birth_year_list[0])
    # calculate most common birth year and count
    most_common_birth_year, most_common_birth_year_events = calculate_name_events_data(df, 'Birth Year')

    # print calculation methods
    # print user type
    print('\n\nUser type statistics:')
    for a, b in user_types_tuples:
        print('\nThere was/were ' + str(b) + ' users of the \"' + str(a) + '\" user type.')
    # print gender type
    print('\n\nUser gender statistics:')
    for a, b in user_gender_tuples:
        print('\nThere was/were ' + str(b) + ' users that were ' + str(a) + '.')
    # print birth years
    print('\n\nUser birth year statistics:')
    print('\nThe earliest user birth year was {}.'.format(most_early_birth_year))
    print('\nThe most recent user birth year was {}.'.format(most_recent_birth_year))
    print('\nThe most common birth year of users was {}, with {} occurrences.'.format(str(int(most_common_birth_year)), most_common_birth_year_events))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n' + ('-'*70))


# main function
def main():
    while True:
        city, month, day = get_filters()

        df = load_data(CITY_DATA, city, month, day)

        # check to see if filtered results returned data, otherwise, exit script
        if df.empty:
            print('\nThere are no results for {} filtered by month: {} and day: {}. Sorry! :-|'.format(city.title(), month.title(), day.title()))
            restart = input('\nWould you like to restart? Enter yes or no.\n\n' + ('-'*70) + '\n')
            if restart.lower() != 'yes':
                break
            else:
                continue

        # run main script functions
        time_stats(df, month, day, city)
        print(input('\nPress enter to continue...'))
        station_stats(df)
        print(input('\nPress enter to continue...'))
        trip_duration_stats(df)
        print(input('\nPress enter to continue...'))
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n\n' + ('-'*70) + '\n')
        if restart.lower() != 'yes':
            break

# main block to call main function
if __name__ == '__main__':
    main()
