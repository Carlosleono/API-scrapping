import requests 
import json
import os
from dotenv import load_dotenv
import pandas as pd
from pandas import json_normalize
from bs4 import BeautifulSoup as bs
import time
import seaborn as sns
from src import functions as f
import matplotlib.pyplot as plt

#Get cases in each country ordered by the average latitude of the country
    #First we obtain a datasets for the mean latitude

covid_data = pd.DataFrame(pd.read_csv('../data/covid_19_clean_complete.csv')).groupby('Country/Region').mean()
covid_data.sort_values(by='Lat', axis=0, inplace = True,)
covid_data.drop(['Confirmed','Deaths','Recovered','Active'], axis=1, inplace=True)
covid_data.reset_index(inplace=True)
covid_data.rename(columns ={'Country/Region':'country'},inplace=True)

    #now we get the same dataset but with the sum of Confirmed, deaths, recovered and active cases
covid_data2 = pd.DataFrame(pd.read_csv('../data/covid_19_clean_complete.csv')).groupby('Country/Region').sum()
covid_data2.reset_index(inplace=True)
covid_data2.drop(['Lat','Long'], axis=1, inplace=True)
covid_data2.rename(columns ={'Country/Region':'country'},inplace=True)
covid_data2
    #next we merge both dataframes by country
covid_data = pd.merge(covid_data, covid_data2, on='country')

# get average temperature by country by using web scrapping
url = "https://en.wikipedia.org/wiki/List_of_countries_by_average_yearly_temperature"
html = requests.get(url)
soup = bs(html.content,"html.parser")

tabla_temps=soup.findAll("table")[0] #we get the first table in the webpage

avTemp = f.averagetemp(tabla_temps)

#mergetables
hyp1 = f.mergedata(covid_data, avTemp)
hyp1['temp'].replace(to_replace='−0.70',value=-0.7, inplace = True)
hyp1['temp'].replace(to_replace='−5.10',value=-5.1, inplace = True)
hyp1['temp'].replace(to_replace='−5.35',value=-5.35, inplace = True)
hyp1['temp'] = hyp1['temp'].astype(float)

# new column 'Zones
hyp1['Zones']  = f.newzones(hyp1['Lat'])

# new columns 'Population' and 'Tests' using webscrapping
poputests = hyp1['country'].apply(f.poptest)
lista=list(poputests)
lista=pd.DataFrame(lista, columns=['Population','Tests'])
hyp1['Population']=lista['Population']
hyp1['Tests']=lista['Tests']

#change data types to float

hyp1['Population'] = f.tofloat(hyp1['Population'])
hyp1['Tests'] = f.tofloat(hyp1['Tests'])
hyp1['Confirmed'] = f.tofloat(hyp1['Confirmed'])
hyp1['Deaths'] = f.tofloat(hyp1['Deaths'])
hyp1['Recovered'] = f.tofloat(hyp1['Recovered'])
hyp1['Active'] = f.tofloat(hyp1['Active'])

#new column 'PositiveRate' and Mortality

hyp1['PositiveRate']=hyp1['Confirmed']/hyp1['Tests']
hyp1['Mortality']=hyp1['Deaths']/hyp1['Confirmed']

# Now we can plot temperature, PositiveRate and Mortality for each Zone, and check if temperature has had an influence in the evolution of Covid-19

hyp1zones=hyp1.groupby('Zones').mean()
hyp1zones.reset_index(inplace=True)
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(20,10))
sns.barplot(x='Zones', y = 'PositiveRate', data=hyp1zones, ax=axs[1]);
sns.barplot(x='Zones', y = 'temp', data=hyp1zones, ax=axs[0]);
sns.barplot(x='Zones', y = 'Mortality', data=hyp1zones, ax=axs[2]);

# Finally we can plot the relation between the number of tests done and the number of recovered people

fig, ax = plt.subplots()
sns.lmplot(x='Tests',y='Recovered', hue='Zones', data=hyp1)
ax.set_xlim(0, 4000000)
ax.set_ylim(0,1000000)
plt.show()

