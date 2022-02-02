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

    while True:
        try:
            city_1 = input('To view the available bikeshare data, Kindly choose one of three cities Chicago, New York City, Washington: ').lower()
            if city_1 in [ 'chicago', 'new york city','washington']:
                break
        except KeyboardInterrupt:
            print('Invalid City Choice!')
        else:
            print('Invalid City Choice!')
    city = city_1



    while True:
        try:
            months = input('Please choose a month to be filtered from \n-January\n-February\n-March\n-April\n-May\n-June\n-All for not filtering by month\n ').lower()
            if months in ['january','february','march', 'april', 'may', 'june', 'all']:
                break
        except:
            print('Please enter a valid month!')
        else:
            print('please enter a valid month name!')
    month = months
    while True:
        try:
            days = input('Please pick a day a day to be filtered \n-Saturday\n-Sunday\n-Monday\n-Tuesday\n-Wednesday\n-Thursday\n-Friday\n-All for not filtering by day\n').lower()
            if days in ['saturady', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']:
                break
        except:
            print('Please enter a valid day')
        else:
            print('Please enter a valid day')
    day = days

    return(city, month, day)

filtered_values = get_filters()
city, month, day = filtered_values

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all' :
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturady', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]
    return df

df = load_data(city, month, day)

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    common_month = df.loc[:,'month'].mode()[0]
    common_day_of_week = df['day_of_week'].mode()[0]
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('Most common month:', common_month)
    print('Most common day:', common_day_of_week)
    print('Most common hour:', common_start_hour)

time_statistics = time_stats(df, month, day)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + [', '] + df['End Station']
    common_combination = df['combination'].mode()[0]

    print('Most used start station:', common_start_station)
    print('Most used end station:', common_end_station)
    print('Most frequent combination of start and end station:', common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
station_statistics = station_stats(df)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Total travel time:', total_time)
    print('Mean travel time:', mean_time )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
trip_statistics = trip_duration_stats(df)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()

    # Display counts of gender
    if city =='washington':
        print('Gender not defined')
    else:
        gender_count = df['Gender'].value_counts()

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('Birth year no defined')
    else:
        earliest_year_of_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('Counts of gender:', gender_count)
        print('Earliest year of birth:', earliest_year_of_birth)
        print('Most recent year of birth:', most_recent_birth)
        print('Mos common year of birth:', common_birth)
    print('Counts of user types:', user_count)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

user_statistics = user_stats(df)

def display_raw_data(city):
    """Raw data is displayed upon request by the user in this manner: Script should prompt the user if they want to see 5 lines of raw data,
     display that data if the answer is 'yes', and continue these prompts and displays until the user says 'no'."""

    display_data = input('May you want to have a look on the raw data?\nType any letter for yes or no to cancel\n').lower()

    while  display_data != 'no':
        try:
            for chunk in pd.read_csv(CITY_DATA[city], chunksize = 5) :

                print(chunk)

                display_data = input('May you want to have a look on the raw data?\nType any letter for yes or no to cancel\n').lower()
                if display_data == 'no':
                    print('Thank you')
                    break




        except KeyboardInterrupt:
            print('Thank you')

display_raw_data(city)

def main():
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    while restart =='yes' :
        get_filters()

        df = load_data(city,month,day)
        time_stats(df, city, month)
        station_stats(df)
        user_stats(df)
        display_raw_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
