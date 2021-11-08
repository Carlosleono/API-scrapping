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

#Get cases in each country ordered by the average latitude of the country

covid_data = pd.DataFrame(pd.read_csv('../data/covid_19_clean_complete.csv')).groupby('Country/Region').mean()
covid_data.sort_values(by='Lat', axis=0, inplace = True,)
covid_data.reset_index(inplace=True)
covid_data.rename(columns ={'Country/Region':'country'},inplace=True)

# get average temperature by country by using web scrapping
url = "https://en.wikipedia.org/wiki/List_of_countries_by_average_yearly_temperature"
html = requests.get(url)
soup = bs(html.content,"html.parser")

tabla_temps=soup.findAll("table")[0] #we get the first table in the webpage

avTemp = f.averagetemp(tabla_temps)

#mergetables
hyp1 = f.mergedata(covid_data, avTemp)

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

#new column 'PositiveRate'

hyp1['PositiveRate']=hyp1['Confirmed']/hyp1['Tests']