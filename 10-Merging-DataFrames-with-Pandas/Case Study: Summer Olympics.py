
'''
We'll be using The Guardian's Olympic medal dataset.
https://www.theguardian.com/sport/datablog/2012/jun/25/olympic-medal-winner-list-data
'''


#Import pandas
import pandas as pd

# Create file path: file_path
# note the file is tab-separated so we assign the delimitter
# For our analysis we do not need the Gold/Silver/Bronze breakdown so we extract just the Grand Total
file_path = 'Summer Olympic medallists 1896 to 2008 - EDITIONS.tsv'
editions = pd.read_csv(file_path,sep='\t')
editions = editions[['Edition','Grand Total','City','Country']]

# Prepare IOC codes table.  Data initially has three columns (including ISO code, which we can disregard)
file_path = 'Summer Olympic medallists 1896 to 2008 - IOC COUNTRY CODES.csv'
ioc_codes = pd.read_csv(file_path)
ioc_codes = ioc_codes[['Country','NOC']]


#-------------------------------------------------------------------------------------------------------------------------

'''
You have a sequence of files summer_1896.csv, summer_1900.csv, ..., summer_2008.csv, one for each Olympic edition (year).
You will build up a dictionary medals_dict with the Olympic editions (years) as keys and DataFrames as values.
The dictionary is built up inside a loop over the year of each Olympic edition (from the Index of editions).
Once the dictionary of DataFrames is built up, you will combine the DataFrames using pd.concat().
'''

# Create empty dictionary: medals_dict
medals_dict = {}

for year in editions['Edition']:

    # Create the file path: file_path
    file_path = 'summer_{:d}.csv'.format(year)
    
    # Load file_path into a DataFrame: medals_dict[year]
    medals_dict[year] = pd.read_csv(file_path)
    
    # Extract relevant columns: medals_dict[year]
    medals_dict[year] = medals_dict[year][['Athlete','NOC','Medal']]
    
    # Assign year to column 'Edition' of medals_dict
    medals_dict[year]['Edition'] = year
    
# Concatenate medals_dict: medals
medals = pd.concat(medals_dict,ignore_index=True)

#-------------------------------------------------------------------------------------------------------------------------

'''
You can extract a Series with the total number of medals awarded in each Olympic edition.
The DataFrame medal_counts can be divided row-wise by the total number of medals awarded each edition;
the method .divide() performs the broadcast as you require.
This gives you a normalized indication of each country's performance in each edition (since the number of medals awarded
each year will vary.
'''

medal_counts = medals.pivot_table(index='Edition',columns='NOC',values='Athlete',aggfunc='count')

# Set Index of editions: totals
totals = editions.set_index('Edition')

# Reassign totals['Grand Total']: totals
totals = totals['Grand Total']

# Divide medal_counts by totals: fractions
fractions = medal_counts.divide(totals,axis='rows')

#-------------------------------------------------------------------------------------------------------------------------

'''
To see if there is a host country advantage, you first want to see how the fraction of medals won changes
from edition to edition.

The expanding mean provides a way to see this down each column.
It is the value of the mean with all the data available up to that point in time. 

Steps:
Create mean_fractions by chaining the methods .expanding().mean() to fractions.
Compute the percentage change in mean_fractions down each column by applying .pct_change() and multiplying by 100. Assign the result to fractions_change.
Reset the index of fractions_change using the .reset_index() method. This will make 'Edition' an ordinary column.
'''

# Apply the expanding mean: mean_fractions
mean_fractions = fractions.expanding().mean()

# Compute the percentage change: fractions_change
fractions_change = mean_fractions.pct_change()*100

# Reset the index of fractions_change: fractions_change
fractions_change = fractions_change.reset_index()


#-------------------------------------------------------------------------------------------------------------------------

'''
Our task here is to prepare a DataFrame hosts by left joining editions and ioc_codes.
Once created, you will subset the Edition and NOC columns and set Edition as the Index.
There are some missing NOC values; you will set those explicitly.
Finally, you'll reset the Index & print the final DataFrame.

Steps:
Create the DataFrame hosts by doing a left join on DataFrames editions and ioc_codes (using pd.merge()).
Clean up hosts by subsetting (Edition and Country) and setting the Index (Edition)
Use the .loc[] accessor to find and manually assign the missing values to the 'NOC' column in hosts.
Reset the index of hosts using .reset_index(), bring Edition back as a column
'''


# Left join editions and ioc_codes: hosts
hosts = pd.merge(editions,ioc_codes,how='left')

# Extract relevant columns and set index: hosts
hosts = hosts[['Edition','NOC']].set_index('Edition')

# Fix missing 'NOC' values of hosts
print(hosts.loc[hosts.NOC.isnull()])
hosts.loc[1972, 'NOC'] = 'FRG'
hosts.loc[1980, 'NOC'] = 'URS'
hosts.loc[1988, 'NOC'] = 'KOR'

# Reset Index of hosts: hosts
hosts = hosts.reset_index()

# Print hosts (now a Data Frame of Edition (years) and Country (hosts))
print(hosts)


#-------------------------------------------------------------------------------------------------------------------------

'''
Our task here is to reshape the fractions_change DataFrame for later analysis.

Initially, fractions_change is a wide DataFrame of 26 rows (one for each Olympic edition) and 139 columns
(one for the edition and 138 for the competing countries).

On reshaping with pd.melt(), as you will see, the result is a tall DataFrame with 3588 rows and 3 columns that
summarizes the fractional change in the expanding mean of the percentage of medals won for each country in blocks.
'''

# Reshape fractions_change: reshaped
reshaped = pd.melt(fractions_change,id_vars='Edition',value_name='Change')

# As an example, create a DataFrame chn by extracting all the rows from reshaped in which the three letter code
# for each country ('NOC') is 'CHN'. 
chn = reshaped[reshaped['NOC']=='CHN']
print(chn.tail())

'''
Output:
         Edition  NOC     Change
    567     1992  CHN   4.240630
    568     1996  CHN   7.860247
    569     2000  CHN  -3.851278
    570     2004  CHN   0.128863
    571     2008  CHN  13.251332
    
We can see that in 2008 (when china last hosted) there was a marked improvement.
'''

#-------------------------------------------------------------------------------------------------------------------------

'''
Merge the reshaped df and hosts.  The end result is a DataFrame summarizing the fractional change in the expanding
mean of the percentage of medals won for the host country in each Olympic edition.
'''

# Merge reshaped and hosts: merged
merged = pd.merge(reshaped,hosts,how='inner')

# Print first 5 rows of merged
print(merged.head())

# Set Index of merged and sort it: influence
influence = merged.set_index('Edition').sort_index()

# Print first 5 rows of influence
print(influence.head())

#-------------------------------------------------------------------------------------------------------------------------

'''

Plot graphs
'''

# Import pyplot
import matplotlib.pyplot as plt

# Extract influence['Change']: change
change = influence['Change']

# Make bar plot of change: ax
ax = change.plot(kind='bar')

# Customize the plot to improve readability
ax.set_ylabel("% Change of Host Country Medal Count")
ax.set_title("Is there a Host Country Advantage?")
ax.set_xticklabels(editions['City'])

# Display the plot
plt.show()
