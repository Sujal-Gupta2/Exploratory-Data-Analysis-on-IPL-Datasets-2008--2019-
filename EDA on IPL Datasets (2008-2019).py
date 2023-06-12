#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis on  IPL ( 2008 - 2019)

# Talk About EDA
# 
# 1. talk about the datasets(what it contains, how it will be useful).
# 2. Calculating missing data percentage value and cleaning it.
# 3. Total number of match played in each seasons.
# 4. No. of tosses won by each team
# 5. Toss decision(field first or bat first) in each seasons.
# 6. We see the team won toss lead to winning matches.
# 7. Which team has won most IPL trophy between(2008-2019)
# 8. Total number of match played in each seasons by each team.
# 9. Total number of win and win % by each team.
# 10. No. of wins at different Venues by a team.( I had only done for MI but, you can do  for every team)
# 11. Maximum Man of the Match Awards by a player.
# 12. Top 5 teams with most wins after batting first.
# 13. Top 5 teams with most wins after batting second.
# 14. Number of matches played in each city.
# 15. Who has umpired most?
# 
# 

# ## Data Preparation and Cleaning
# 
# 1. Load the file using Pandas
# 2. Look at some information about the data and the columns
# 3. Fix any missing or incorrect values

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, plot, iplot
from plotly import tools
from warnings import filterwarnings
filterwarnings('ignore')


# In[2]:


ipl = pd.read_csv('matches.csv',encoding = "utf-8")


# In[3]:


ipl.head()


# In[4]:


ipl.shape


# In[5]:


ipl.columns


# In[6]:


ipl.info()


# The column date has datatype of objec. Changing to datetime data type.

# In[7]:


ipl['date']= pd.to_datetime(ipl['date'])


# In[8]:


ipl.info()


# In[9]:


matches= ipl.isnull()
matches.head(20)


# 'False' means the value is not missing and 'True' means the value is missing

# ## Counting missing value in each column

# In[10]:


for column in matches.columns.values.tolist():
    print(column)
    print(matches[column].value_counts())
    print(" ")


# In[11]:


missing_percentages= ipl.isna().sum().sort_values(ascending=False) /len(ipl) 
missing_percentages


# In[12]:


type(missing_percentages)


# In[13]:


missing_percentages[missing_percentages !=0].plot(kind='barh')


# ## Remove upmire3 column as too many missing value and for other column missing values are deleted

# In[14]:


ipl.__delitem__('umpire3')


# In[15]:


ipl.head()


# In[16]:


ipl.dropna( subset=["city", "winner", "player_of_match", "umpire1", "umpire2"], inplace=True)


# In[17]:


ipl.shape


# In[18]:


ipl.isna().sum()


# you can see there are no null values or empty space

# In[19]:


ipl.describe()


# # Exploratory Visualization And Analysis
# 
# 
# columns we analyze
# 
# 1. Player_of_match
# 2. result
# 3. toss_winner
# 4. win_by_runs
# 5. winner
# 6. win_by_wickets
# 7. season
# 8. city
# 9. team
# 10. toss_decision
# 11. venue
# 12. umpire1 and umpire2
# 

# In[20]:


ipl['season'] = pd.DatetimeIndex(ipl['date']).year
ipl.head()


# In[21]:


match_per_season=ipl.groupby(['season'])['id'].count().reset_index().rename(columns={'id':'matches'})
match_per_season.style.background_gradient(cmap='PuBu')


# In[22]:


colors = ['turquoise',] * 13
colors[5] = 'crimson'

fig=px.bar(data_frame=match_per_season,x=match_per_season.season,y=match_per_season.matches,labels=dict(x="Season",y="Count"),)
fig.update_layout(title="Number of matches played in different seasons ",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# Each season, almost 60 matches were played. However, we see a spike in the number of matches from 2011 to 2013. This is because two new franchises, the Pune Warriors and Kochi Tuskers Kerala, were introduced, increasing the number of teams to 10.

# In[23]:


ipl['toss_winner'].value_counts()


# In[24]:


toss=ipl['toss_winner'].value_counts()
colors = ['turquoise',] * 15
colors[0] = 'crimson'
fig=px.bar( y=toss,x=toss.index,labels=dict(x="Season",y="Count"),)
fig.update_layout(title="No. of tosses won by each team",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# Mumbai Indians have won the most tosses, followed by Kolkata Knight Riders.

# In[25]:




temp_series = ipl.toss_decision.value_counts()
labels = (np.array(temp_series.index))
values = (np.array((temp_series / temp_series.sum())*100))
colors = ['turquoise', 'crimson']
fig = go.Figure(data=[go.Pie(labels=labels,
                             values=values,hole=.3)])
fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=3)))
fig.update_layout(title="Toss decision percentage",
                  titlefont={'size': 30},
                  )
fig.show()


# After winning the toss, team tends to field first

# In[26]:


fig=px.histogram(data_frame=ipl,x='season',color='toss_decision',color_discrete_sequence=colors,barmode='group')
fig.update_layout(title="Toss decision in different seasons",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1)
fig.show()


# Most of the times, teams decide to field first, except in season 2009,2010,2013 where teams decided to bat first mostly.
# Since 2014, teams have overwhelmingly chosen to bat second. Especially since 2016, teams have chosen to field for more than 80% of the times.

# In[27]:


labels =["Yes",'No']
values = ipl['winner'].value_counts()
colors = ['turquoise', 'crimson']
fig = go.Figure(data=[go.Pie(labels=labels,
                             values=values,hole=.3)])
fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=3)))
fig.update_layout(title="Winning toss implies winning macthes?",
                  titlefont={'size': 30},
                  )
fig.show()


# In[28]:


ipl['result'].value_counts()


# In[29]:


winning_teams =ipl[['season','winner']]

#dictionaries to get winners to each season
winners_team = {}
for i in sorted(winning_teams.season.unique()):
    winners_team[i] = winning_teams[winning_teams.season == i]['winner'].tail(1).values[0]
    
winners_of_IPL = pd.Series(winners_team)
winners_of_IPL = pd.DataFrame(winners_of_IPL, columns=['team'])


# In[30]:


winners_of_IPL.value_counts().index


# In[31]:


colors = ['turquoise',] * 6
colors[0] = 'crimson'
fig=px.bar( y=winners_of_IPL['team'].value_counts(),x=winners_of_IPL['team'].value_counts().index,labels=dict(x="Team Name",y="Count"),)
fig.update_layout(title="Winners of IPL",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# Mumbai Indians won IPL for 4 times, followed by Chennai Super Kings for 3 times and Kolkata Knight Riders for 2 times.

# In[32]:


matches_played_byteams=pd.concat([ipl['team1'],ipl['team2']],axis=1)
teams=(matches_played_byteams['team1'].value_counts()+matches_played_byteams['team2'].value_counts()).reset_index()
teams.columns=['Team Name','Total Matches played']
teams.sort_values(by=['Total Matches played'],ascending=False).reset_index().drop('index',axis=1).style.background_gradient(cmap='PuBu')


# In[33]:


wins=pd.DataFrame(ipl['winner'].value_counts()).reset_index()
wins.columns=['Team Name','Wins']
wins.style.background_gradient(cmap='PuBu')


# In[34]:


played=teams.merge(wins,left_on='Team Name',right_on='Team Name',how='inner')
played['% Win']=(played['Wins']/played['Total Matches played'])*100
played.sort_values(by=['% Win'],ascending=False).reset_index().drop('index',axis=1).style.background_gradient(cmap='PuBu',subset=['% Win'])


# In[35]:


colors = ['turquoise',] * 15
colors[8] = 'crimson'
fig=px.bar(x=played['Team Name'],y=played['Total Matches played'],labels=dict(x="Team Name",y="Count"),)
fig.update_layout(title="Total number of matches played",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# In[36]:


colors = ['turquoise',] * 15
colors[8] = 'crimson'
fig=px.bar(x=played['Team Name'],y=played['Wins'],labels=dict(x="Team Name",y="Count"),)
fig.update_layout(title="Total Win by teams",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# In[37]:


colors = ['turquoise',] * 15
colors[-4] = 'crimson'
fig=px.bar(x=played['Team Name'],y=played['% Win'],labels=dict(x="Team Name",y="Count"),)
fig.update_layout(title="Win % by teams",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# Rising Pune Supergiants have the highest win % of 62.50, followed by Chennai Super kings, Delhi Capitals and Mumbai Indians.
# This is largely due to the fact that they had played really few matches.

# In[38]:


def lucky(ipl,team_name):
    return ipl[ipl['winner']==team_name]['venue'].value_counts().nlargest(10)


# In[39]:


mi=lucky(ipl,'Mumbai Indians')
values = mi
labels=mi.index
colors = ['turquoise', 'crimson']
fig = go.Figure(data=[go.Pie(labels=labels,values=values,hole=.3)])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=3)))
fig.update_layout(title="Wins at different Venues for MI:",
                  titlefont={'size': 30},
                  )
fig.show()


# In[40]:


toss=ipl['player_of_match'].value_counts()[0:10]
colors = ['turquoise',] * 10
colors[0] = 'crimson'
fig=px.bar( y=toss,x=toss.index,labels=dict(x="Player_Name",y="Count"),)
fig.update_layout(title="Maximum Man of the Match Awards",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# In[41]:


#Extracting the records where a team won batting first
batting_first=ipl[ipl['win_by_runs']!=0]


# In[42]:


batting_first.head()


# In[43]:


batting_first['winner'].value_counts()


# In[44]:


first=batting_first['winner'].value_counts()[0:5]
colors = ['turquoise',] * 10
colors[0] = 'crimson'
fig=px.bar( y=first,x=first.index,labels=dict(x="Team",y="Count"),)
fig.update_layout(title="Top 5 teams with most wins after batting first",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# In[45]:


#extracting those records where a team has won after batting second
batting_second=ipl[ipl['win_by_wickets']!=0]
batting_second.head()


# In[46]:


second=batting_second['winner'].value_counts()[0:5]
colors = ['turquoise',] * 10
colors[0] = 'crimson'
fig=px.bar( y=second,x=second.index,labels=dict(x="Team",y="Count"),)
fig.update_layout(title="Top 5 teams with most wins after batting second",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# In[47]:


city=ipl['city'].value_counts()[0:5]
colors = ['turquoise',] * 10
colors[0] = 'crimson'
fig=px.bar( y=city,x=city.index,labels=dict(x="City",y="Count"),)
fig.update_layout(title="Number of matches played in each city",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()


# In[48]:


ump=pd.concat([ipl['umpire1'],ipl['umpire2']])
ump=ump.value_counts()
umps=ump.to_frame().reset_index()
ump.head(10)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




