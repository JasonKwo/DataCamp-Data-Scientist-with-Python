
# data_file path and file has been pre-loaded - saved in github https://github.com/JasonKwo/DataCamp-Data-Scientist-with-Python/blob/master/8-Pandas-Foundations/1981-2010%20NOAA%20Austin%20Climate%20Normals.csv
# df_climate file saved https://github.com/JasonKwo/DataCamp-Data-Scientist-with-Python/blob/master/8-Pandas-Foundations/weather_data_austin_2010.csv

# Import pandas
import pandas as pd

# Read in the data file: df
df = pd.read_csv(data_file)
print(df.head())

# Notice that there are no column headers
# Read in the data file with header=None: df_headers
df_headers = pd.read_csv(data_file, header=None)

# Print the output of df_headers.head()
# Now it looks sensible
print(df_headers.head())

#column_labels str has been pre-loaded
column_labels = 'Wban,date,Time,StationType,sky_condition,sky_conditionFlag,visibility,visibilityFlag,wx_and_obst_to_vision,wx_and_obst_to_visionFlag,dry_bulb_faren,dry_bulb_farenFlag,dry_bulb_cel,dry_bulb_celFlag,wet_bulb_faren,wet_bulb_farenFlag,wet_bulb_cel,wet_bulb_celFlag,dew_point_faren,dew_point_farenFlag,dew_point_cel,dew_point_celFlag,relative_humidity,relative_humidityFlag,wind_speed,wind_speedFlag,wind_direction,wind_directionFlag,value_for_wind_character,value_for_wind_characterFlag,station_pressure,station_pressureFlag,pressure_tendency,pressure_tendencyFlag,presschange,presschangeFlag,sea_level_pressure,sea_level_pressureFlag,record_type,hourly_precip,hourly_precipFlag,altimeter,altimeterFlag,junk'

# list_to_drop list has been pre-loaded
list_to_drop = ['sky_conditionFlag', 'visibilityFlag', 'wx_and_obst_to_vision', 'wx_and_obst_to_visionFlag',
                'dry_bulb_farenFlag', 'dry_bulb_celFlag', 'wet_bulb_farenFlag', 'wet_bulb_celFlag', 'dew_point_farenFlag',
                'dew_point_celFlag', 'relative_humidityFlag', 'wind_speedFlag', 'wind_directionFlag',
                'value_for_wind_character', 'value_for_wind_characterFlag', 'station_pressureFlag', 'pressure_tendencyFlag',
                'pressure_tendency', 'presschange', 'presschangeFlag', 'sea_level_pressureFlag', 'hourly_precip',
                'hourly_precipFlag', 'altimeter', 'record_type', 'altimeterFlag', 'junk']

# Split on the comma to create a list: column_labels_list
column_labels_list = column_labels.split(',')

# Assign the new column labels to the DataFrame: df.columns
df.columns = column_labels_list

# Remove the appropriate columns: df_dropped
df_dropped = df.drop(list_to_drop, axis='columns')

# Print the output of df_dropped.head()
# We now have 17 columns, down from 44
print(df_dropped.head())

# 'date' column is currently an integer
# Let's convert it first to a string
df_dropped['date'].head()
df_dropped['date'] = df_dropped['date'].astype(str)

# 'Time' is also an integer
# Add leading zeros to convert into a usable format
df_dropped['Time'].head()
df_dropped['Time'] = df_dropped['Time'].apply(lambda x:'{:0>4}'.format(x))


# Concatenate the new date and Time columns: date_string
date_string = df_dropped['date'] + df_dropped['Time']

# Convert the date_string Series to datetime: date_times
date_times = pd.to_datetime(date_string, format='%Y%m%d%H%M')

# Set the index to be the new date_times container: df_clean
df_clean = df_dropped.set_index(date_times)

# Print the output of df_clean.head()
print(df_clean.head())




# The numeric columns contain missing values labeled as 'M'.  Our job is to transform these columns
# such that they contain only numeric values and interpret missing data as NaN.

# Print the dry_bulb_faren temperature between 8 AM and 9 AM on June 20, 2011
print(df_clean.loc['2011-6-20 08:00':'2011-6-20 09:00', 'dry_bulb_faren'])

# Convert the dry_bulb_faren column to numeric values: df_clean['dry_bulb_faren']
df_clean['dry_bulb_faren'] = pd.to_numeric(df_clean['dry_bulb_faren'], errors='coerce')

# Print the transformed dry_bulb_faren temperature between 8 AM and 9 AM on June 20, 2011
print(df_clean.loc['2011-6-20 08:00':'2011-6-20 09:00', 'dry_bulb_faren'])

# Convert the wind_speed and dew_point_faren columns to numeric values
df_clean['wind_speed'] = pd.to_numeric(df_clean['wind_speed'], errors='coerce')
df_clean['dew_point_faren'] = pd.to_numeric(df_clean['dew_point_faren'], errors='coerce')


#------------------------------------------------------------------------------------------------------------------------

# Some Exploratory Data Analysis

# Print the median of the dry_bulb_faren column
print(df_clean['dry_bulb_faren'].median())

# Print the median of the dry_bulb_faren column for the time range '2011-Apr':'2011-Jun'
print(df_clean.loc['2011-Apr':'2011-Jun', 'dry_bulb_faren'].median())

# Print the median of the dry_bulb_faren column for the month of January
print(df_clean.loc['2011-Jan', 'dry_bulb_faren'].median())




# Compare 2011 with 2010
# Extract as Numpy arrays since date index doesn't match

# Downsample df_clean by day and aggregate by mean: daily_mean_2011
daily_mean_2011 = df_clean.resample('d').mean()

# Extract the dry_bulb_faren column from daily_mean_2011 using .values: daily_temp_2011
daily_temp_2011 = daily_mean_2011['dry_bulb_faren'].values

# Downsample df_climate by day and aggregate by mean: daily_climate
daily_climate = df_climate.resample('d').mean()

# Extract the Temperature column from daily_climate using .reset_index(): daily_temp_climate
daily_temp_climate = daily_climate.reset_index().Temperature

# Compute the difference between the two arrays and print the mean difference
difference = daily_temp_2011 - daily_temp_climate
print(difference.mean())



# Compare temperature when it is sunny or not

# Using df_clean, when is sky_condition 'CLR'?
is_sky_clear = df_clean['sky_condition']=='CLR'
# Filter df_clean using is_sky_clear
sunny = df_clean.loc[is_sky_clear]
# Resample sunny by day then calculate the max
sunny_daily_max = sunny.resample('d').max()
# See the result
sunny_daily_max.head()


# Using df_clean, when does sky_condition contain 'OVC'?
is_sky_overcast = df_clean['sky_condition'].str.contains('OVC')
# Filter df_clean using is_sky_overcast
overcast = df_clean.loc[is_sky_overcast]
# Resample overcast by day then calculate the max
overcast_daily_max = overcast.resample('d').max()
# See the result
overcast_daily_max.head()


# Calculate the mean of sunny_daily_max
sunny_daily_max_mean = sunny_daily_max.mean()

# Calculate the mean of overcast_daily_max
overcast_daily_max_mean = overcast_daily_max.mean()

# Print the difference (sunny minus overcast)
print(sunny_daily_max_mean - overcast_daily_max_mean)

# result: dry_bulb_faren is on average 6.5 degrees hotter on sunny days than overcast days


#------------------------------------------------------------------------------------------------------------------------

# Time for some visual EDA

# check correlation between visibility and temp
# Import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# Select the visibility and dry_bulb_faren columns and resample them: weekly_mean
weekly_mean = df_clean[['visibility','dry_bulb_faren']].resample('W').mean()

# Print the output of weekly_mean.corr()
print(weekly_mean.corr())

# Plot weekly_mean with subplots=True
weekly_mean.plot(subplots=True)
plt.show()



# Explore and visualise fraction of sunny hours on clear days

# Using df_clean, when is sky_condition 'CLR'?
is_sky_clear = df_clean['sky_condition'] == 'CLR'
# Resample is_sky_clear by day
resampled = is_sky_clear.resample('D')
# See the result
resampled

# Calculate the number of sunny hours per day
sunny_hours = resampled.sum()
# Calculate the number of measured hours per day
total_hours = resampled.count()
# Calculate the fraction of hours per day that were sunny
sunny_fraction = sunny_hours / total_hours

# Make a box plot of sunny_fraction
sunny_fraction.plot(kind='box')
plt.show()


# Dew point is a measure of relative humidity based on pressure and temperature.
# A dew point above 65 is considered uncomfortable while a temperature above 90 is also considered uncomfortable.

# Resample dew_point_faren and dry_bulb_faren by Month, aggregating the maximum values: monthly_max
monthly_max = df_clean[['dew_point_faren','dry_bulb_faren']].resample('M').max()
# Generate a histogram with bins=8, alpha=0.5, subplots=True
monthly_max.plot(kind='hist',bins=8,alpha=0.5,subplots=True)
# Show the plot
plt.show()




# Extract the maximum temperature in August 2010 from df_climate: august_max
august_max = df_climate['Temperature'].loc['2010-08'].max()
print(august_max)

# Resample August 2011 temps in df_clean by day & aggregate the max value: august_2011
august_2011 = df_clean.loc['2011-08','dry_bulb_faren'].resample('D').max()


# Filter for days in august_2011 where the value exceeds august_max: august_2011_high

august_2011_high = august_2011[august_2011>august_max]

# Construct a CDF of august_2011_high
august_2011_high.plot(kind='hist',normed=True, cumulative=True,bins=25)

# Display the plot
plt.show()

