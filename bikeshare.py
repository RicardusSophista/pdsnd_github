import time
import pandas as pd
import numpy as np
import datetime as dt
import utils as u

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
    city = u.get_input('Choose a city from the following options: Chicago, New York City, Washington.',
                    ['Chicago','New York City','Washington']).lower()


    month = u.get_input('Choose a month from between January to June to view statistics for a specific month,\nor input \'all\' to view statistics for all months',
                      ['January','February','March','April','May','June','All']).title()


    day = u.get_input('Choose a day of the week to view statistics for a specific day,\nor input \'all\' to view statistics for all months',
                   ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']).title()


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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    df['trip'] = df['Start Station'] + ' to ' + df['End Station']


    if month != 'All':
        df = df[df['month']==month]

    if day != 'All':
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print(u.mode_text('month to travel',df['month'].mode()))

    print(u.mode_text('day of the week to travel',df['day_of_week'].mode()))


    raw_mode = df['hour'].mode()
    format_mode = [str(m).rjust(2,'0') + ':00 - ' + str(m).rjust(2,'0') + ':59' for m in raw_mode]
    print(u.mode_text('hour of the day to start a trip',format_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    input("Press ENTER to continue.")
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print(u.mode_text('start station',df['Start Station'].mode()))



    print(u.mode_text('end station',df['End Station'].mode()))


    print(u.mode_text('trip',df['trip'].mode()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    input("Press ENTER to continue.")
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    tot = u.format_time(dt.timedelta(seconds=float(df['Trip Duration'].sum())))
    print('Total travel time is ',tot)


    mn = u.format_time(dt.timedelta(seconds=float(df['Trip Duration'].mean())))
    print('Mean travel time is ',mn)


    print("\nThis took %s seconds." % (time.time() - start_time))
    input('Press ENTER to continue.')
    print('-'*40)




def user_stats(df):
    """Displays statistics on bikeshare users."""


    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('User types are broken down as follows:')
    print(u.table_builder(['User Type', 'Count'],df['User Type'].value_counts().to_dict()))

    cols = df.columns
    if all(c in cols for c in ['Gender','Birth Year']) == False:
        print('Unfortunately, this dataset does not contain information about gender or age.')
        return

    df['Gender'].fillna('Not specified', inplace=True)
    df['Birth Year'] = df['Birth Year'].fillna(0).apply(lambda x: int(x))


    print('\n\nThe gender of users is divided as follows:')
    print(u.table_builder(['Gender','Count'],df['Gender'].value_counts().to_dict()))
    print("\nThis took %s seconds." % (time.time() - start_time))

    input('\nPress ENTER to continue.')

    # TO DO: Display earliest, most recent, and most common year of birth
    sane_df = df[df['Birth Year']>0]

    earliest = sane_df['Birth Year'].min()
    print('The earliest year of birth is {}.'.format(earliest))
    sanity = u.get_input('Does this value make sense Y/N?',['Y','N']).upper()
    if sanity == 'N':
        guess = u.get_int('What would you accept as the earliest possible birth year?',min=earliest)
        sane_df = sane_df[sane_df['Birth Year']>=guess]
        earliest = sane_df['Birth Year'].min()
        print('The earliest birth year in the data is ',earliest)

    latest = df['Birth Year'].max()
    print('The most recent year of birth is {}.'.format(latest))
    sanity = u.get_input('Does this value make sense Y/N?',['Y','N']).upper()
    if sanity == 'N':
        guess = u.get_int('What would you accept as the most recent possible birth year?',max=latest)
        sane_df = sane_df[sane_df['Birth Year'] <= guess]
        latest = sane_df['Birth Year'].max()
        print('The most recent plausible birth year is ',latest)

    print(u.mode_text('year of birth',sane_df['Birth Year'].mode()))

    input("Press ENTER to continue.")

    print('Calculating average trip duration by year of birth.')

    bin_list = np.arange(earliest, latest+10, 10)
    bin_labels = [str(x) + ' - ' + str(x+9) for x in bin_list[:-1]]
    t_by_y = sane_df.groupby(pd.cut(sane_df['Birth Year'],bins=bin_list, labels=bin_labels))['Trip Duration'].mean().apply(lambda x: u.format_time(dt.timedelta(seconds=x)))

    print(u.table_builder(['Birth Year','Average Trip Duration'],t_by_y.to_dict()))

    print('-'*40)

def raw_data(raw):
    """ Returns the rows of the dataframe 'raw', 5 at a time, until the user gets fed up"""
    c = 'Y'
    row = 0
    end = len(raw)
    while c == 'Y' and row < end:
        for i in range(5):
            print(raw.iloc[row,])
            row += 1
            if row == end:
                print('There are no further rows to display')
                break
        c = u.get_input('Continue Y/N?',['Y','N'])


def main():
    go = 'Y'
    while go == 'Y':
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        r = u.get_input('Would you like to view the raw data Y/N?',['Y','N'])
        if r == 'Y':
            raw_df = pd.read_csv(CITY_DATA[city])
            raw_data(raw_df)

        go = u.get_input('\nWould you like to restart Y/N?',['Y','N'])



if __name__ == "__main__":
	main()
