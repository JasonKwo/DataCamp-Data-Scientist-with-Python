# Analysing Olympic data provided by the Guardian


# Simple count of medals by country
country_names = medals['NOC']
medal_counts = country_names.value_counts()
print(medal_counts.head(15))



# Construct the pivot table: counted
counted = medals.pivot_table(index='NOC',values='Athlete',columns='Medal',aggfunc='count')

# Create the new column: counted['totals']
counted['totals'] = counted.sum(axis='columns')

# Sort counted by the 'totals' column
counted = counted.sort_values('totals', ascending=False)

# Print the top 15 rows of counted
print(counted.head(15))
