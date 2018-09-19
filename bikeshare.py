import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.  User is given the option to filter by month, or by day, or by (month and day), or none.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """

    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington) and use while loop to check for invalid entries

    while True:
        city = input('What city would you like to explore? Type Chicago, New York City, or Washington:\n')

        # make sure city value is all lower case so that dictionary lookup on line 110 of load_data function works as expected

        city = city.lower()

        if city not in ('chicago', 'new york city', 'washington'):
            print("I didn\'t catch that - try again.\n")
        else:
            # Input as expected so break out of while loop - we got a valid input city
            # Note user can use any number of capital letter and it doesn't matter since the .lower() string method is used
            break

    # get data filter option user input.  The local variable filter is used to capture the filter options of month or day or (month and day) or none

    # while look used to validate inputs

    while True:
        filter = input('Would you like to filter the data by month, day, month and day (both), or not at all? Type Month, Day, Both, or None: \n')
        if filter.lower() not in ('month', 'day', 'both', 'none'):
            print("I didn\'t catch that - try again.\n")
        else:
            # Input as expected so break out of while loop - we got a valid filter option
            break

    # if statement used to process the different filter options and set month and city variable to correct value

    if filter.lower() in ('both'):
        # get user input for month and day
        while True:
            month = input('\nWhich month? January, February, March, April, May, or June? Type full month name.\n')
            month = month.lower()
            if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("I didn\'t catch that - try again.\n")
            else:
                # Input as expected so break out of while loop - we got a valid month option
                break
        while True:
            day = input('\nWhich Day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Type full day name.\n')
            if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                print("I didn\'t catch that - try again.\n")
            else:
                # Input as expected so break out of while loop - we got a valid day of week option
                break

    elif filter.lower() in ('day'):
        # get user input for just the day
        while True:
            day = input('\nWhich Day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Type full day name.\n')
            if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                print("I didn\'t catch that - try again.\n")
            else:
                # Input as expected so break out of while loop - we got a valid day of week option
                # assing all to month
                month = 'all'
                break
    elif filter.lower() in ('month'):
        # get user input for just the month
        while True:
            month = input('\nWhich month? January, February, March, April, May, or June? Type full month name.\n')
            month = month.lower()
            if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("I didn\'t catch that - try again.\n")
            else:
                # Input as expected so break out of while loop - we got a valid month option
                # assign all to day
                day = 'all'
                break
    elif filter.lower() in ('none'):
        # assign all to to month and day
        month = 'all'
        day = 'all'

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert the end Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # calculate trip duration from Start Time and End Time and create new column total_dur with this data

    df['total_dur'] = df['End Time'] - df['Start Time']

    # df['total_dur'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time']) - this code also worked too but not needed since I previously convert times to datetime format

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # month = month.lower()  # make sure month is all lower case
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month: ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day Of Week: ', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Common End Station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df_route = df[['Start Station','End Station']]
    df_route1 = df_route.groupby(['Start Station','End Station']).size().nlargest(1).reset_index(name='Count')
    print('Most Common Combination Of Start And End Stations:\n ')
    print(df_route1)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['total_dur'].sum()
    print('The Total Travel Time is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['total_dur'].mean()
    print('The Average Travel Time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    print('Note: Gender and Birthday Stats not available for Washington\n')

    # df = df.fillna(0)

    start_time = time.time()

    # Display counts of user types

    user_types_counts = df['User Type'].value_counts()
    print('The Counts By User Type Are: \n', user_types_counts)

    # below if statement to deal with no gender or birth data in washington, passed city varible into the user_stats function to be able to make this check

    if city != "washington":

        # Display counts of gender
        gender_types_counts = df['Gender'].value_counts()
        print('\nThe Counts By Gender Type Are: \n', gender_types_counts)

        # Display earliest, most recent, and most common year of birth

        print('\n')
        earliest_bday = df['Birth Year'].min()
        print('The Oldest Birthday was: ', earliest_bday)

        most_recent_bday = df['Birth Year'].max()
        print('The Yongest (Most Recent) Birthday was: ', most_recent_bday)

        most_common_bday = df['Birth Year'].mode()[0]
        print('The Most Common Birthday was: ', most_common_bday)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        # pass city to user_stats to check if city if Washington so that gender and birth stats are not calculated in this use case
        user_stats(df,city)

        # see if user wants to see raw data, while loop for input validation
        while True:
            see_data = input('\nWould You Like To See The Data? Enter Y or N:\n')
            if see_data.lower() not in ('y','n'):
                print("I didn\'t catch that - try again.\n")
            else:
                # got expected input exit while loop
                break  # user doesn't want to restart so end program

        # let user enter # of rows to view, while loop for input validation
        if see_data in ('y'):
            while True:
                view_n_rows = int(input('\nEnter Number Of Rows:\n'))
                if (view_n_rows > 299999 or view_n_rows < 1):
                    print('Number has to be between 1 and 299999 - try again.\n')
                else:
                    break
            print(df.head(view_n_rows))

        # below while loop for input validation
        while True:
            restart = input('\nWould you like to restart? Enter Y or N.\n')
            if restart.lower() not in ('y', 'n'):
                print("I didn\'t catch that - try again.\n")
            else:
                # got expected input exit while loop
                break  # user doesn't want to restart so end program

        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
