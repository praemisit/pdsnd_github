"""This is the bikeshare module which explores data related to bike share 
systems for three major cities in the United States: Chicago, 
New York City, and Washington.

The module was developed as part of the Udacity nanodegree 
"Programming for Data Science".

Author: Bertram Kaup
Email: Bertram.Kaup@bayer.com

Required input files: 'chicago.csv', 'new_york_city.csv', 'washington.csv' 
"""
import time
import datetime as dt
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
    print('Hello! Let\'s explore some US bikeshare data from Chicago, New York City or Washington!')

    # Get user input for which city (chicago, new york city, washington) the analysis shall be done.
    while True:
        city = input("Which city do you like to analyze? Chicago, New York City or Washington?\n")
        if city in ['Chicago', 'New York City', 'Washington']:
            print("Cool - thanks for your input. Your analysis will focus on city {}.".format(city))
            city = city.lower()
            break
        else:
            print("I couldn't get your input. Please make sure to only input one of the three cities Chicago, New York City or Washington.")

    # Get user input for for which month (all, january, february, ... , june) the analysis shall be done.
    while True:
        # First ask the user whether he/she wants to filter by month, by day, by both or not at all
        month_day = input("Do you like to filter the data by month, day, both, or not at all? Type \"none\" for no time filter.\n")
        # Check whether the input was valid. If not, ask the user again.
        if month_day not in ['month', 'day', 'both', 'none']:
            print("I couldn't get your input. Please make sure to only input \"month\" \"day\", \"both\", or \"none\".")
        else:
            # In case of no filter on month and day, set the return values to 'all'
            if month_day == 'none':
                month = 'all'
                day = 'all'
            break
            
    # Only if the user wants to filter by month, get input for which month the analysis shall be done
    if month_day == 'month' or month_day == 'both':
        while True:
            # Ask the user for which month the analysis shall be done
            month = input("Which month? Please type \"all\", \"January\", \"February\", \"March\", \"April\", \"May\", or \"June\".\n")
            # Check whether the input was valid. If not, ask the user again.
            if month not in ['all', 'January', 'February', 'March', 'May', 'June']:
                print("I couldn't get your input. Please make sure to only input \"all\", \"January\", \"February\", \"March\", \"April\", \"May\", or \"June\".")
            else:
                month = month.lower()
                break
    else:
        # Set month to all, if the user does not want to filter by month
        month = 'all'
            
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    # Only ask for day of week, if the user had specified that he/she wants to filter accordingly
    if month_day == 'day' or month_day == 'both':
        days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        while True:
            day_string = input("Which day of the week? Please type your response as an integer with 1=Sunday and 7=Saturday.\n")
            # Check whether the input was valid. If not, ask the user again.
            if day_string not in ['1','2','3','4','5','6','7']:
                print("I couldn't get your input. Please make sure to only input an integer value between 1 and 7. (1=Sunday; ... 7=Saturday).")
            else:
                # Convert the input into the name of the week day
                day = days[int(day_string)-1]
                day = day.lower()
                break
    else:
        # Set day to all, if the day shall not be filtered
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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
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

    print('-'*40)
    print('\nCalculating The Most Frequent Times of Travel...\n\n')
    start_time = time.time()
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day, and hour from the Start Time column to create  respective columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # Calculate and display the most common month
    popular_month = df['month'].value_counts().idxmax()
    popular_month_count = df['month'].value_counts().max()
    # use the index of the months list to get the corresponding month name
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print("Most popular month has been {} with {} trips.".format(months[int(popular_month)-1], popular_month_count))

    # Calculate and display the most common day of week
    popular_day = df['day'].value_counts().idxmax()
    popular_day_count = df['day'].value_counts().max()
    print("Most popular day of the week has been {} with {} trips.".format(popular_day, popular_day_count))


    # Calculate and display the most common start hour
    popular_hour = df['hour'].value_counts().idxmax()
    popular_hour_count = df['hour'].value_counts().max()
    print("Most popular hour has been {} with {} trips.".format(popular_hour, popular_hour_count))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('-'*40)
    print('\nCalculating The Most Popular Stations and Trip...\n\n')
    start_time = time.time()

    # Calculate and display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    popular_start_station_count = df['Start Station'].value_counts().max()
    print("The most popular start station has been \"{}\" with {} trips.".format(popular_start_station, popular_start_station_count))


    # Calculate and display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    popular_end_station_count = df['End Station'].value_counts().max()
    print("The most popular end station has been \"{}\" with {} trips.".format(popular_end_station, popular_end_station_count))


    # Calculate and display most frequent combination of start station and end station trip
    # Logic: 
    # The start-end combination is created by an additional column in df data frame. 
    # Start- and end station are seperated by a "____" string, so that they can be 
    # split again for printing.
    df['Station Combination'] = df['Start Station'] + '____' + df['End Station']
    popular_combination = df['Station Combination'].value_counts().idxmax()
    popular_combination_count = df['Station Combination'].value_counts().max()
    print("The most popular start-/ end station combination was from \"{}\" to \"{}\" with {} trips.".format(popular_combination.split('____')[0],  popular_combination.split('____')[1], popular_combination_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('-'*40)
    print('\nCalculating Trip Duration...\n\n')
    start_time = time.time()

    # Calculate and display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time has been {} seconds.'.format(total_travel_time))

    # Calculate and display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Average travel time per trip has been {} seconds.'.format(average_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('-'*40)
    print('\nCalculating User Stats...\n\n')
    start_time = time.time()

    # Calculate and display counts of user types
    print("Overview of trips by user types:")
    print(df.groupby(['User Type'])['User Type'].count())


    # Calculate and display counts of gender
    # As some cities might not provide that information, check first whether the data exists
    if 'Gender' in df.columns:
        print("Overview of trips by gender:")
        print(df.groupby(['Gender'])['Gender'].count())
    else:
        print("No gender information available.")

    # Calculate and display earliest, most recent, and most common year of birth
    # As some cities might not provide that information, check first whether the data exists
    if 'Birth Year' in df.columns:
        print("The earliest year of birth is: {}".format(int(df['Birth Year'].min())))
        print("The most recent year of birth is: {}".format(int(df['Birth Year'].max())))
        print("The most common year of birth is: {}".format(int(df['Birth Year'].mode())))
    else:
        print("No Birth Year information available")          

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
        
        # Show raw data if the user likes
        row_counter = 0
        while True:
            show_raw_data = input("\nIf you want to see some raw data, please type y or yes. Otherwise just type return.\n")
            if show_raw_data.lower() == 'yes' or show_raw_data.lower() == 'y':
                print(df.iloc[row_counter:row_counter+5])
                row_counter+=5
            else:
                break
        restart = input('\nIf you want to restart the script, please type y or yes. Otherwise just type return.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
