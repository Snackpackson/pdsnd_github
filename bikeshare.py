import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        try:
            cities = ['Chicago', 'New York City', 'Washington']
            city = input('Please select a city\n> {} \n> '.format(cities)).lower()
            if 'new york' in city:
                city = 'new york city'
            if city.title() in cities:
                break
            else:
                print('\nYour selection was not valid. Please try again.')
        finally:
            print('\nYou selected {}.\n'.format(city.title()))

    while True:
        try:
            months = ['January', 'February', 'March', 'April', 'May', 'June']
            month = input('Please select a month or enter "All"\n> {} \n> '.format(months)).title()
            if month in months:
                break
            if 'All' in month:
                break
            else:
                print('\nYour selection was not valid. Please try again.')
        finally:
            print('\nYou selected {}.\n'.format(month.title()))

    while True:
        try:
            days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            day = input('Please select a day of the week or enter "All"\n> {} \n> '.format(days)).title()
            if day in days:
                break
            if 'All' in day:
                break
            else:
                print('\nYour selection was not valid. Please try again.')
        finally:
            print('\nYou selected {}.\n'.format(day.title()))

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
    df = pd.read_csv(CITY_DATA[city])
    df = pd.DataFrame(df)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'All':
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day = days.index(day) + 1
        df = df[df['day'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print('The most common month is:',common_month)

    common_day = df['day'].mode()[0]
    print('The most common day is:',common_day)

    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour is:', df['hour'].mode()[0])

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is:\n{}'.format(popular_start))

    popular_end = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is:\n{}'.format(popular_end))

    df['combination'] = 'Start:' + df['Start Station'] + '\nEnd:' + df['End Station']
    print('\nThe most most frequent combination of start station and end station is:\n{}'.format((df['combination'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('The sum of the trip durations is: {} seconds'.format(df['Trip Duration'].sum()))

    print('The mean travel time is: {} seconds'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('The count of users by type is:\n{}\n'.format(df['User Type'].value_counts()))

    if 'Gender' in df.columns:
        print('The count of users by gender is:\n{}\n'.format(df['Gender'].value_counts()))

    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        print('The earliest year of birth is:', int(birth_year.min()))
        print('The most recent year of birth is:', int(birth_year.max()))
        print('The most common year of birth is:', int(birth_year.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        view_data = input('\nWould you like to view the data?\nEnter yes or no.\n> ').lower()
        print('\nYou selected {}.'.format(view_data))
        start_loc = 0
        while True:
            try:
                if 'yes' in view_data:
                    print(df.iloc[start_loc:start_loc + 5])
                    start_loc += 5
                    view_data = input('\nWould you like to view more data?\nEnter yes or no.\n> ').lower()
                else:
                    print('\nYour selection was not valid. Please try again.')
                    view_data = input('\nWould you like to view the data?\nEnter yes or no.\n> ').lower()
            finally:
                print('\nYou selected {}.'.format(view_data))
                if 'yes' in view_data:
                    print()
                if 'no' in view_data:
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
