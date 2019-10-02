'''
You're now going to revisit the sales data you worked with earlier in the chapter.
Three DataFrames jan, feb, and mar have been pre-loaded for you.
Your task is to aggregate the sum of all sales over the 'Company' column into a single DataFrame.
You'll do this by constructing a dictionary of these DataFrames and then concatenating them.
'''



# Make the list of tuples: month_list
month_list = [('january',jan),('february',feb),('march',mar)]

# Create an empty dictionary: month_dict
month_dict = {}

for month_name, month_data in month_list:

    # Group month_data: month_dict[month_name]
    month_dict[month_name] = month_data.groupby('Company').sum()

# Concatenate data in month_dict: sales
sales = pd.concat(month_dict)

# Print sales
print(sales)

# Print all sales by Mediacore
idx = pd.IndexSlice
print(sales.loc[idx[:, 'Mediacore'], :])

#-------------------------------------------------------------------------------------------------------------------------

'''
In this exercise, you'll compare the historical 10-year GDP (Gross Domestic Product) growth in the US and in China.
The data for the US starts in 1947 and is recorded quarterly; by contrast, the data for China starts in 1961 and is
recorded annually.

You'll need to use a combination of resampling and an inner join to align the index labels. You'll need an appropriate
offset alias for resampling, and the method .resample() must be chained with some kind of aggregation method (.pct_change()
and .last() in this case).

pandas has been imported as pd, and the DataFrames china and us have been pre-loaded,
'''


# Resample and tidy china: china_annual
# Chain resample (to get annual sample), last (to take last data point data), pct_change(10) (to compute
# the percentage change with an offset of ten years), and dropna (to remove null values)
china_annual = china.resample('A').last().pct_change(10).dropna()

# Resample and tidy us: us_annual
us_annual = us.resample('A').last().pct_change(10).dropna()

# Concatenate china_annual and us_annual: gdp
gdp = pd.concat([china_annual,us_annual],join='inner',axis=1)

# Resample gdp and print
print(gdp.resample('10A').last())
