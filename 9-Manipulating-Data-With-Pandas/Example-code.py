#Transform columns and filter outliers using zscore 

# Import zscore
from scipy.stats import zscore

# Group gapminder_2010 data by region and transform the life and fertility columns using zscore
standardized = gapminder_2010.groupby('region')[['life','fertility']].transform(zscore)

# Construct a Boolean Series to identify outliers: outliers
outliers = (standardized['life'] < -3) | (standardized['fertility'] > 3)

# Filter gapminder_2010 by the outliers: gm_outliers
gm_outliers = gapminder_2010.loc[outliers]

#------------------------------------------------------------------------------------------------------

#Fill missing data using median
#Here we fill missing age data for titanic passengers using the median for the sex and cabin class


# Create a groupby object: by_sex_class
by_sex_class = titanic.groupby(['sex','pclass'])

# We can view summary of the groupby object
by_sex_class['age'].describe()

# Write a function that imputes median
def impute_median(series):
    return series.fillna(series.median())

# Impute age and assign to titanic['age']
titanic.age = by_sex_class['age'].transform(impute_median)

# Print the output of titanic.tail(10)
print(titanic.tail(10))

#------------------------------------------------------------------------------------------------------

#Other transformations with .apply

# In this exercise, you're going to analyze economic disparity within regions of the world using the Gapminder data set for
# 2010. To do this you'll define a function to compute the aggregate spread of per capita GDP in each region and the individual
# country's z-score of the regional per capita GDP. You'll then select three countries - United States, Great Britain and
# China - to see a summary of the regional GDP and that country's z-score against the regional mean.


def disparity(gr):
    # Compute the spread of gr['gdp']: s
    s = gr['gdp'].max() - gr['gdp'].min()
    # Compute the z-score of gr['gdp'] as (gr['gdp']-gr['gdp'].mean())/gr['gdp'].std(): z
    z = (gr['gdp'] - gr['gdp'].mean())/gr['gdp'].std()
    # Return a DataFrame with the inputs {'z(gdp)':z, 'regional spread(gdp)':s}
    return pd.DataFrame({'z(gdp)':z , 'regional spread(gdp)':s})


# Group gapminder_2010 by 'region': regional
regional = gapminder_2010.groupby('region')

# Apply the disparity function on regional: reg_disp
reg_disp = regional.apply(disparity)

# Print the disparity of 'United States', 'United Kingdom', and 'China'
print(reg_disp.loc[['United States','United Kingdom','China']])


#------------------------------------------------------------------------------------------------------
#Grouping and filtering with .apply()
# In this exercise you'll take the Titanic data set and analyze survival rates from the 'C' deck,
# which contained the most passengers, by sex.


def c_deck_survival(gr):
    c_passengers = gr['cabin'].str.startswith('C').fillna(False)
    return gr.loc[c_passengers, 'survived'].mean()

# Create a groupby object using titanic over the 'sex' column: by_sex
by_sex = titanic.groupby('sex')

# Call by_sex.apply with the function c_deck_survival
c_surv_by_sex = by_sex.apply(c_deck_survival)

# Print the survival rates
print(c_surv_by_sex)

#------------------------------------------------------------------------------------------------------

# Grouping and filtering with .filter()

# Read the CSV file into a DataFrame: sales
sales = pd.read_csv('sales.csv', index_col='Date', parse_dates=True)

# Group sales by 'Company': by_company
by_company = sales.groupby('Company')

# Compute the sum of the 'Units' of by_company: by_com_sum
by_com_sum = by_company['Units'].sum()
print(by_com_sum)

# Filter 'Units' where the sum is > 35: by_com_filt
by_com_filt = by_company.filter(lambda g: g['Units'].sum() > 35)
print(by_com_filt)


#------------------------------------------------------------------------------------------------------

# Filtering and grouping with .map()

#Create the Boolean Series: under10
under10 = titanic['age']<10
under10= under10.map({True:'under 10',False:'over 10'})

# Group by under10 and compute the survival rate
survived_mean_1 = titanic.groupby(under10)['survived'].mean()
print(survived_mean_1)

# Group by under10 and pclass and compute the survival rate
survived_mean_2 = titanic.groupby([under10,'pclass'])['survived'].mean()
print(survived_mean_2)












