import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input('\nPlease enter one of the valid cities name: Chicago, New York City or Washington: ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid input. Please try again.')
        
    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nPlease enter a month (like January, February, March, April, May, June, All): ').lower()
        if month in MONTHS_DATA:
            break
        else:
            print('Invalid input. Please try again.')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nPlease enter any day of the week or All to show all days: ').lower()
        if day in DAYS_DATA:
            break
        else:
            print('Invalid input. Please try again.')

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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of the week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name+

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['Month'] == month]
    # Filter by day of week if applicable
    if day != 'all':

        # Filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

           
    # Display the most common month
    # This code will show most common month only when user will use 'All' as input
    # If single month is used, it will only show that month 
    common_month = df['Month'].mode()[0]
    month_name = calendar.month_name[common_month]
    print(f'\nMost popular month for traveling is: {month_name}.')
    
    # Display the most common day of week
    # This code will show most common day only when user will use 'All' as input
    # If single day is used, it will only show that day 
    common_day = df['Day of Week'].mode()[0]
    print(f'\nMost popular day for traveling is: {common_day}.')
    
    # Display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_start_hour = df['Hour'].mode()[0]
    print(f'\nMost popular start hour for traveling is: {common_start_hour}.')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_popular_startstation = df['Start Station'].mode()[0]
    print(f'\nMost popular start station is: {most_popular_startstation}.')

    # Display most commonly used end station
    most_popular_endstation = df['End Station'].mode()[0]
    print(f'\nMost popular end station is: {most_popular_endstation}.')

    # Display most frequent combination of start station and end station trip
    freq_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'\nMost frequent trip combination is from {freq_combination[0]} to {freq_combination[1]}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel = df['Trip Duration'].sum()

    #Finds out the duration in minutes and seconds format
    minute, second = divmod(total_travel, 60)
    #Finds out the duration in hour and minutes format

    hour, minute = divmod(minute, 60)
    
    print(f"\nThe total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    # Display mean travel time
    avg_travel = df['Trip Duration'].mean()

    #Finds the average duration in minutes and seconds format
    mins, sec = divmod(avg_travel, 60)
  
    if mins > 60:
        hrs, mins = divmod(minute, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {round(sec, 0)} seconds.")
        
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('\nCount of user types is: \n')
    print(user_type_count)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nGender count is: \n')
        print(gender_count)
    else:
        print("\nGender type doesn\'t exist.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode())
        print(f'\n The earliest birthday year is: {earliest_year}.')
        print(f'\n The most recent birthday year is: {recent_year}.')
        print(f'\n The most common birthday year is: {common_year}.')
    else:
        print("\nNo birth year data avaialble.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function to display the data frame itself as per user request
def display_data(df):
    """
    Displays 5 rows of data from the dataframe at a time and asks the user if they want to see more.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    start_loc = 0
    while True:
        # Input accepts yes or no, or YES or NO
        show_data = input("Would you like to see 5 rows of raw data? Enter yes or no: ").lower()
        if show_data != 'yes':
            break
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        if start_loc >= len(df):
            print("You've reached the end of the data.")
            break
            

# Last main funtcion to call all other functions 
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
