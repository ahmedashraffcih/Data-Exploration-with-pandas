import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'Dataset/chicago.csv',
              'new york city': 'Dataset/new_york_city.csv',
              'washington': 'Dataset/washington.csv' }
             
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Intializing empty variable to store city choice
    city = '' # STORE INPUT VALUE 

    print("Hello! Let\'s explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city.lower() not in CITY_DATA.keys():
        print("\nWelcome to this program.Please choose your city:")
        print("\n- Chicago OR New York City OR Washington")
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nPlease check your input, it doesn\'t appear to be conforming to any of the accepted input formats.")
            print("\nAccepted input:\nFull name of city; not case sensitive (e.g. chicago or CHICAGO).\nFull name in title case (e.g. Chicago).")
            print("\nRestarting...")

    print("\nYou have chosen {} as your city.".format(city.title()))

    # get user input for month (all, january, february, ... , june)
    #Creating a dictionary to store all the months including the 'all' option
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}

    # Intializing empty variable to store month choice
    month = '' # STORE INPUT VALUE 

    while month not in MONTH_DATA.keys():
        print("\nPlease enter the month, between January to June, for which you're seeking the data:")
        print("\n(You may also view data for all months, please type 'all' for that.)")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nInvalid input. Please try again in the accepted input format.")
            print("\nRestarting...")

    print(f"\nYou have chosen {month.title()} as your month.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    #Creating a list to store all the days including the 'all' option
    DAYS_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # Intializing empty variable to store city choice
    day = '' # STORE INPUT VALUE 

    while day not in DAYS_DATA:
        print("\nPlease enter a day in the week of your choice for which you're seeking the data:")
        print("\n(You may also view data for all days, please type 'all' for that.)")
        day = input().lower()

        if day not in DAYS_DATA:
            print("\nInvalid input. Please try again in one of the accepted input formats.")
            print("\nRestarting...")

    print("\nYou have chosen {} as your day.".format(day.title()))
    print("\nYou have chosen to view data for city: {}, month/s: {} and day/s: {}.".format(city.upper(),month.upper(),day.upper()))
    print("-"*40)
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
    #Load data for city
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

     #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()


    # display the most common month
    common_month = df['month'].mode()[0]

    print("Most Common Month: {}".format(common_month))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]

    print("\nMost Common Day: {}".format(common_day))
    
    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # display the most common start hour
    common_hour = df['hour'].mode()[0]

    print("\nMost Common Start Hour: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print("The most commonly used start station: {}".format(common_start_station))


    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print("\nThe most commonly used end station: {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    #str.cat to combine two columsn in the df 
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    comb = df['Start To End'].mode()[0]

    print("\nThe most frequent combination of trips are from {}.".format(comb))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()

    #Finds out the duration in minutes and seconds format
    minute, second = divmod(total_duration, 60)
    #Finds out the duration in hour and minutes format
    hour, minute = divmod(minute, 60)

    print("The total trip duration is {} hours, {} minutes and {} seconds.".format(hour,minute,second))
    
    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())

    #Finds the average duration in minutes and seconds format
    mins, sec = divmod(average_duration, 60)

    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print("\nThe average trip duration is {} hours, {} minutes and {} seconds.".format(hrs,mins,sec))
    else:
        print("\nThe average trip duration is {} minutes and {} seconds.".format(mins,sec))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nThe types of users by gender are:\n\n{}".format(gender))
    except:
        print("\nThere is no 'Gender' column in this file.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth: {}\n\nThe most recent year of birth: {}\n\nThe most common year of birth: {}".format(earliest,recent,common_year))
    except:
        print("There are no birth year details in this file.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def display_raw_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the raw data?")
        print("\nAccepted responses:\nYes or yes\nNo or no")
        rdata = input().lower()
        #the raw data from the df is displayed if user opts for it
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")

    #Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")

        if restart.lower() == 'yes':
            continue
        elif restart.lower() == 'no':
            break
        else:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            break


if __name__ == "__main__":
	main()