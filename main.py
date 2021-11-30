#importing some functions
#defined in functions.py
from functions import *
import sys
import io
import subprocess
import os

# implement pip as a subprocess to install dep's
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'pandas', 'requests', 'openpyxl'])
import pandas as pd
import urllib
import zipfile
import datetime
import requests
from datetime import date
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
from pathlib import Path


#TODO set this up for retrieving last year's data

todays_date = date.today()
today_year= todays_date.year
last_year = (today_year -1)
# print(last_year)



dataFolder =Path("C:/Users/Public/Documents/"+str(last_year)+"/")  #local dev storage location

#Checking for folder exist and creating if not

# Check whether the specified path exists or not
isExist = os.path.exists(dataFolder)

if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(dataFolder)


##########################################################################################
#Begin EIA emissions data mining
##########################################################################################

#load in EIA emissions data
#TODO change to variable year
urlEmissions = 'https://www.eia.gov/electricity/data/emissions/xls/emissions'+str(last_year)+'.xlsx'

#load emissions data from EIA
#TODO allow more years?, change function to specific...etc.
df=loadDataframe(urlEmissions,'CO2',1,str)

#explicitly converting to numbers
df['Tons of CO2 Emissions'] = pd.to_numeric(df['Tons of CO2 Emissions'], errors= 'coerce')
df['Generation (kWh)'] = pd.to_numeric(df['Generation (kWh)'], errors= 'coerce')


#filtering for only MISO controlled plants
miso_df = df[df['Balancing Authority Code']=='MISO']

#calculation of emissions (lbs/kWhr) assuming abs(generation to account for generation facility using power)
miso_df['CO2 Emissions/kwhr (pounds/kWhr)'] = (miso_df['Tons of CO2 Emissions']/(abs(miso_df['Generation (kWh)'])))*2000

#filtering by fuel type
miso_PET = miso_df[miso_df['Aggregated Fuel Group']=='PET']
miso_GAS = miso_df[miso_df['Aggregated Fuel Group']=='GAS']
miso_COAL = miso_df[miso_df['Aggregated Fuel Group']=='COAL']
miso_MSW = miso_df[miso_df['Aggregated Fuel Group']=='MSW']

#Filtering by region
MN = miso_df[miso_df['State'] == 'MN']
ND = miso_df[miso_df['State'] == 'ND']
SD = miso_df[miso_df['State'] == 'SD']
MT = miso_df[miso_df['State'] == 'MT']
IA = miso_df[miso_df['State'] == 'IA']
IL = miso_df[miso_df['State'] == 'IL']
IN = miso_df[miso_df['State'] == 'IN']
WI = miso_df[miso_df['State'] == 'WI']
MI = miso_df[miso_df['State'] == 'MI']
MO = miso_df[miso_df['State'] == 'MO']
AR = miso_df[miso_df['State'] == 'AR']
MS = miso_df[miso_df['State'] == 'MS']
LA = miso_df[miso_df['State'] == 'LA']
TX = miso_df[miso_df['State'] == 'TX']
KY = miso_df[miso_df['State'] == 'KY']

miso_North = pd.concat([MN,ND, SD, MT, IA])
miso_Central = pd.concat([WI,MI, IL, IN, KY, MO])
miso_South = pd.concat([AR, MS, LA, TX])

#saving to csv for manual
df.to_csv(dataFolder / "EIA_raw.csv", encoding='utf-8', index=False)
miso_df.to_csv(dataFolder / "EIA_miso_filt_ALL.csv", encoding='utf-8', index=False)
miso_PET.to_csv(dataFolder / "EIA_miso_filt_PET.csv", encoding='utf-8', index=False)
miso_GAS.to_csv(dataFolder / "EIA_miso_filt_GAS.csv", encoding='utf-8', index=False)
miso_COAL.to_csv(dataFolder / "EIA_miso_filt_COAL.csv", encoding='utf-8', index=False)
miso_MSW.to_csv(dataFolder / "EIA_miso_filt_MSW.csv", encoding='utf-8', index=False)
miso_North.to_csv(dataFolder/"EIA_miso_filt_north.csv", encoding='utf-8', index=False)
miso_Central.to_csv(dataFolder/"EIA_miso_filt_central.csv", encoding='utf-8', index=False)
miso_South.to_csv(dataFolder/"EIA_miso_filt_south.csv", encoding='utf-8', index=False)

#convert to csv for manual verification
#printing to console for dev
print(miso_df['Plant Code'])

##########################################################################################
#Begin EIA plant data mining
##########################################################################################


# # User list comprehension to create a list of lists from Dataframe rows
# list_of_rows = [list(row) for row in newdf.values]
# # Insert Column names as first list in list of lists
# list_of_rows.insert(0, newdf.columns.to_list())
# # Print list of lists i.e. rows
# print(list_of_rows[0])
# #print ()