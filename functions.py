# devFunctions.py>

# functions

def loadDataframe(url,sheetName, skiprow, dtype):
    import pandas as pd
    # load in EIA emissions data from previous year
    df = pd.read_excel('https://www.eia.gov/electricity/data/emissions/xls/emissions2020.xlsx',sheet_name = sheetName, skiprows=skiprow, dtype=dtype)
    #do some stuff here
    print(url)
    return df
