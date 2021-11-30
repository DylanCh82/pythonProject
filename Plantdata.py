# importing some functions
# defined in functions.py
import os.path

from functions import *
import sys
import io
import subprocess

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

# TODO set this up for retrieving last year's data

# todays_date = date.today()
# today_year= todays_date.year
# last_year = (today_year -1)
# print(last_year)


dataFolder = Path("C:/Users/Public/Documents/")  # local dev storage location

##########################################################################################
# Begin EIA PLANT data mining
##########################################################################################
#
# #load in EIA plant data
# #TODO change to variable year


#dev if statement to reduce wait times on dev
#create pickle file name
pickle_file = ("testpickle1.pkl")
#check to see if pickle exists (returns bool)
pickleExists = os.path.isfile(dataFolder / "testpickle1.pkl")

#if the file doesn't exist we do this code
if not pickleExists:
    urlData = 'https://www.eia.gov/electricity/data/eia860/xls/eia8602020.zip'  # link to EIA plant data
    getfolder = requests.get(urlData)
    archive = zipfile.ZipFile(io.BytesIO(getfolder.content))
    xlfile = archive.open('2___Plant_Y2020.xlsx')
    df2 = pd.read_excel(xlfile, skiprows=1)
    #store pickle
    df2.to_pickle(dataFolder / pickle_file)
#if the file already exists we load it and save time
else:
    df2 = pd.read_pickle(dataFolder / "testpickle1.pkl")

#now back to manipulation
df2 = df2[df2['Balancing Authority Code'] == 'MISO']
print(df2)
dropCols = [0, 1, *range(14, len(df2.columns), 1)]
df2 = df2.drop(df2.columns[dropCols], axis=1)
df2.to_csv(dataFolder / "EIA_plant_MISO.csv", encoding='utf-8', index=False)
print(df2)
# #load emissions data from EIA
# #TODO allow more years?, change function to specific...etc.
# df=loadDataframe(urlEmissions,1,str)
#
# #explicitly converting to numbers
# df['Tons of CO2 Emissions'] = pd.to_numeric(df['Tons of CO2 Emissions'], errors= 'coerce')
# df['Generation (kWh)'] = pd.to_numeric(df['Generation (kWh)'], errors= 'coerce')
#
# #filtering for only MISO controlled plants
# miso_df = df[df['Balancing Authority Code']=='MISO']
#
# #calculation of emissions (lbs/kWhr) assuming abs(generation to account for generation facility using power)
# miso_df['Emissions/kwhr (pounds/kWhr)'] = (miso_df['Tons of CO2 Emissions']/(abs(miso_df['Generation (kWh)'])))*2000
#
# #filtering by fuel type
# miso_PET = miso_df[miso_df['Aggregated Fuel Group']=='PET']
# miso_GAS = miso_df[miso_df['Aggregated Fuel Group']=='GAS']
# miso_COAL = miso_df[miso_df['Aggregated Fuel Group']=='COAL']
# miso_MSW = miso_df[miso_df['Aggregated Fuel Group']=='MSW']
#
# #saving to csv for manual
# df.to_csv(dataFolder / "EIA_raw.csv", encoding='utf-8', index=False)
# miso_df.to_csv(dataFolder / "EIA_miso_filt_ALL.csv", encoding='utf-8', index=False)
# miso_PET.to_csv(dataFolder / "EIA_miso_filt_PET.csv", encoding='utf-8', index=False)
# miso_GAS.to_csv(dataFolder / "EIA_miso_filt_GAS.csv", encoding='utf-8', index=False)
# miso_COAL.to_csv(dataFolder / "EIA_miso_filt_COAL.csv", encoding='utf-8', index=False)
# miso_MSW.to_csv(dataFolder / "EIA_miso_filt_MSW.csv", encoding='utf-8', index=False)
# #convert to csv for manual verification
# #printing to console for dev
# print(miso_df['Plant Code'])
