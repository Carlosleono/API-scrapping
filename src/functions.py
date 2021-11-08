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

def averagetemp(x):
    '''
    This function gets a table and returns a dataframe 
    '''
    temperature=[]
    for f in x.findAll('tr')[1:]: #list with all rows in the table
        country = f.findAll('td')[0].getText().strip()
        temp = f.findAll('td')[1].getText().strip()

        diccionario = {"country": country, "temp": temp}

        temperature.append(diccionario)
    avTemp = pd.DataFrame(temperature)
    return avTemp

def mergedata(x,y):
    '''
    This function merge two datasets
    '''
    hyp1=pd.merge(x, y, on="country")
    
    return hyp1

def newzones(x):
    '''
    This functions generate a new column from a dataset based on its latitude classifying by geographical zone
    '''
    Zones = []
    for l in range(0,len(x)):
        if x[l] < -66.5:
            Zones.append('Antarctic')
        elif x[l] < -23.55:
            Zones.append('South Temperate')
        elif x[l] < 0:
            Zones.append('South Tropic')
        elif x[l] < 23.55:
            Zones.append('North Tropic')
        elif x[l] < 66.5:
            Zones.append('North Temperate')
        else:
            Zones.append('Artic')
    return Zones

def poptest(x):
    '''
    This function return the pòpulation and number of tests done from a country passed to the function
    '''
    time.sleep(1.1)
    url = "https://covid-193.p.rapidapi.com/history"

    querystring = {f"country":{x},"day":"2020-11-08"} #Database values are from a year ago

    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "c626d6c478msh5f1aa9758ec0e22p1e219ajsn0ed4c7e9c605"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    
    try:
        return (response['response'][0]['population'],response['response'][0]['tests']['total'])
        
    except:
        return ('NaN', 'NaN')
    
def tofloat(x):
    '''This function changes a pandas series to float
    '''

    return x.astype(float)