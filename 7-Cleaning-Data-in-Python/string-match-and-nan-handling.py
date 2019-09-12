import re
import numpy as np

# If doing multiple times e.g. row-wise in a DataFrame, compile the pattern first
# ^ means to start at the beginning of the string
# $ means finish at the end of the string
# without these two, the string could be in the middle of other text, rather than explicit
# \$ 'escapes the dollar symbol'
# \d{n} is digit n times
# \d* is digit any numer of times
# \d+ recognises 10 as 10 rather than 1 and 0
# [A-Z] is capital letter
# \w* is is alphanumeric any numer of times

pattern1 = re.compile('^\$\d*\.\d{2}$')
check1 = bool(pattern1.match('$1234.56'))

pattern2 = re.findall('\d+','There are 10 strawberries and 2 bananas')
# returns ['10','2']
# note that these are strings


#------------------------------------------------------------------------------------------------------------

#Replace using Function

# Define recode_gender()
def recode_gender(gender):

    # Return 0 if gender is 'Female'
    if gender == 'Female':
        return 0
    
    # Return 1 if gender is 'Male'    
    elif gender == 'Male':
        return 1
    
    # Return np.nan    
    else:
        return np.nan

# Apply the function to the sex column
tips['recode'] = tips.sex.apply(recode_gender)


#------------------------------------------------------------------------------------------------------------

# Write the lambda function using replace
tips['total_dollar_replace'] = tips.total_dollar.apply(lambda x: x.replace('$', ''))

# Write the lambda function using regular expressions
tips['total_dollar_re'] = tips.total_dollar.apply(lambda x: re.findall('\d+\.\d+', x)[0])

#------------------------------------------------------------------------------------------------------------

DataFrame.drop_duplicates()
# Calculate the mean of the Ozone column: oz_mean
oz_mean = airquality.Ozone.mean()

# Replace all the missing values in the Ozone column with the mean
airquality['Ozone'] = airquality.Ozone.fillna(oz_mean)

# .notnull() checks for missing values
# chaining .all() checks the entire row
# and another for the entire table
#assert returns nothing if true or error if false
assert pd.notnull(df).all().all() # or df.notnull().all().all()


