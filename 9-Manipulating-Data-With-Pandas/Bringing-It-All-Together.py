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

#------------------------------------------------------------------------------------------------------------------

# We have two columns: Gender and Event_Gender.  Investigate.

# Select columns: ev_gen
ev_gen = medals[['Event_gender','Gender']]
ev_gen_uniques = ev_gen.drop_duplicates()
print(ev_gen_uniques)


# Alternately, group medals by the two columns: medals_by_gender
medals_by_gender = medals.groupby(['Event_gender','Gender'])
medal_count_by_gender = medals_by_gender.count()
print(medal_count_by_gender)

# Create the Boolean Series: sus
sus = (medals.Event_gender == 'W') & (medals.Gender == 'Men')

# Create a DataFrame with the suspicious row: suspect
suspect = medals[sus]

# Print suspect
print(suspect)

#------------------------------------------------------------------------------------------------------------------

# Use .nunique() to return the number of disctinct categories

country_grouped = medals.groupby('NOC')
Nsports = country_grouped['Sport'].nunique()
Nsports = Nsport.sort_values(ascending=False)
print(Nsports)


#Compare USA vs USSR during cold war

# Create a Boolean Series that is True when 'Edition' is between 1952 and 1988: during_cold_war
during_cold_war = (medals.Edition >= 1952) & (medals.Edition <= 1988)

# Extract rows for which 'NOC' is either 'USA' or 'URS': is_usa_urs
is_usa_urs = medals.NOC.isin(['USA','URS'])

# Use during_cold_war and is_usa_urs to create the DataFrame: cold_war_medals
cold_war_medals = medals.loc[during_cold_war & is_usa_urs]

# Group cold_war_medals by 'NOC'
country_grouped = cold_war_medals.groupby('NOC')

# Create Nsports
Nsports = country_grouped.nunique()['Sport']

# Print Nsports
print(Nsports)


#------------------------------------------------------------------------------------------------------------------
# See who won more medals consistently

# Create the pivot table: medals_won_by_country
medals_won_by_country = medals.pivot_table(index='Edition',columns='NOC',values='Athlete',aggfunc='count')

# Slice medals_won_by_country: cold_war_usa_urs_medals
cold_war_usa_urs_medals = medals_won_by_country.loc[1952:1988, ['USA','URS']]

# Create most_medals 
most_medals = cold_war_usa_urs_medals.idxmax(axis='columns')

# Print most_medals.value_counts()
print(most_medals.value_counts())


#------------------------------------------------------------------------------------------------------------------


# Create the DataFrame: usa
usa = medals[medals['NOC'] == 'USA']

# Group usa by ['Edition', 'Medal'] and aggregate over 'Athlete'
usa_medals_by_year = usa.groupby(['Edition','Medal'])['Athlete'].count()

# Reshape usa_medals_by_year by unstacking
usa_medals_by_year = usa_medals_by_year.unstack(level='Medal')

# Plot the DataFrame usa_medals_by_year
usa_medals_by_year.plot()
plt.show()

usa_medals_by_year.plot.area()
plt.show()

#------------------------------------------------------------------------------------------------------------------

# medal order is currently alphabetical
# can re-order using categories

# Redefine 'Medal' as an ordered categorical
medals.Medal = pd.Categorical(values=medals['Medal'],
                              categories=['Bronze','Silver','Gold'],
                              ordered=True)

usa_medals_by_year.plot.area()
plt.show()
