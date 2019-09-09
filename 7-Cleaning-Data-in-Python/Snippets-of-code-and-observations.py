import pandas as pd

df = pd.read_csv('')

df.head()
df.tail()
df.shape
df.columns

# Information about your data frame.  Can be used to make quick observations such as an expect float/int column being
# categorised as objects or the count of non-null values not matching the row count.
df.info()

# Two equivalent ways of count in descending order the count of values in a particular column
df.continent.value_counts(dropna=False) # This will include any missing values in the count
df['continent'].value_counts(dropna=False)


df.country.value_counts(dropna=False).head() # We would expect each country to only have one entry, but in our
                                             # example 'Sweden' has count 2, requiring further investigation
                                             


df.describe() # Shows summary statistics of numerical columns



#------------------------------------------------------------------------------------------------------------------------#

#plotting histograms

# Import matplotlib.pyplot
import matplotlib.pyplot as plt

# Describe the column
df['Existing Zoning Sqft'].describe()

# Plot the histogram
df['Existing Zoning Sqft'].plot(kind='hist', rot=70, logx=True, logy=True)

# Display the histogram
plt.show()

#------------------------------------------------------------------------------------------------------------------------#


# Create the boxplot
df.boxplot(column='initial_cost', by='Borough', rot=90)

# Display the plot
plt.show()

df.plot(kind='scatter', x='initial_cost', y='total_est_fee', rot=70)
plt.show()

#------------------------------------------------------------------------------------------------------------------------#

# Melt airquality: airquality_melt
airquality_melt = pd.melt(airquality, id_vars=['Month', 'Day'], var_name='measurement', value_name='reading')


# Pivot airquality_melt: airquality_pivot
# We use .pivot_table() instead of .pivot() since .pivot() doesn't know how to handle duplicate entries.
# .pivot_table() on the other hand can be passed a parameter to handle this e.g. aggfunc=np.mean
airquality_pivot = airquality_melt.pivot_table(index=['Month','Day'], columns='measurement', values='reading')

#------------------------------------------------------------------------------------------------------------------------#

# The pivot creates a DataFrame with a hierarchal index (similar to Excel Pivot Tables).  To revert back to the original
# table format, we can reset the index.


# Reset the index of airquality_pivot: airquality_pivot_reset
airquality_pivot_reset = airquality_pivot.reset_index()

# Print the index of airquality_pivot
print(airquality_pivot.index)

# Print the new index of airquality_pivot_reset
print(airquality_pivot_reset.index)



#------------------------------------------------------------------------------------------------------------------------#

airquality_pivot = airquality_dup.pivot_table(index=['Month', 'Day'], columns='measurement', values='reading', aggfunc=np.mean)
airquality_pivot = airquality_pivot.reset_index()




#------------------------------------------------------------------------------------------------------------------------#

# Melt ebola: ebola_melt
ebola_melt = pd.melt(ebola, id_vars=['Date', 'Day'], var_name='type_country', value_name='counts')

# Create the 'str_split' column
ebola_melt['str_split'] = ebola_melt.type_country.str.split('_')

# Create the 'type' column
ebola_melt['type'] = ebola_melt.str_split.str.get(0)

# Create the 'country' column
ebola_melt['country'] = ebola_melt.str_split.str.get(1)

# Print the head of ebola_melt
print(ebola_melt.head())

