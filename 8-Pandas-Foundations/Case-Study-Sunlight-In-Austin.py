
#data_file path and file has been pre-loaded
#saved in github https://github.com/JasonKwo/DataCamp-Data-Scientist-with-Python/blob/master/Pandas-Foundations/1981-2010%20NOAA%20Austin%20Climate%20Normals.csv

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
