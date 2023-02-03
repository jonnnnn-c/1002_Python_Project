import pandas as pd
import os


#Clean Crime Rates Data and extract data
def cleanCSVdata(filename,country,startyear,endyear):
    df = pd.read_csv(filename,skiprows=16)
    #print(df[" Per 100K Population"][3])
    datasetstartyear = int((df["date"][0])[:4])
    datasetendyear = int((df["date"][len(df["date"])-1])[:4])
    #ensure the year range is appropriate for the dataset
    startyear,endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)

    print(endyear)

    print(datasetendyear)
    startrow = startyear - datasetstartyear
    print(datasetstartyear)
    newdata = []

    for year in range(endyear-startyear+1):
        newdata.append(float(df[" Per 100K Population"][startrow+year]))

    return newdata

#Clean CPI Data XLSX and extract data
def cleanCPIdata(filename,startyear,endyear):
    df = pd.read_excel(filename)
    #print(df.loc[1][1]) #starts from column 1 row 4, get value from start of each year so column = 12*n-1, starting from when crime rates starts recording
    newdata = []
    datasetstartcol = 0

    ####Finds for which col the data starts to show

    for i in range(1,len(df.loc[4])):
        #print(df.loc[4][i])
        if str(df.loc[4][i]) != 'nan':
            datasetstartcol = i
            break
    
    datasetstartyear = int((df.loc[1][datasetstartcol])[:4])
    datasetstartmonth = int((df.loc[1][datasetstartcol])[-2:])
    datasetendyear = int((df.loc[1][len(df.loc[1])-1])[:4])
    
    startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)

    startcol = datasetstartcol + (13-datasetstartmonth+(startyear-datasetstartyear-1)*12)
    

    ###Append data into list

    for year in range(endyear-startyear+1):
        #newdata.append(float(df.loc[4][startcol+year*12]))
        newdata.append(float(df.loc[4][startcol+year*12]))

    return newdata

#Clean Income Inequality Data XLSX and extract data
def cleanIncomedata(filename,country,startyear,endyear):
    startyear, endyear = int(startyear), int(endyear)
    df = pd.read_excel(filename, sheet_name="Data")
    countrylist = df["Country"]
    newdata = []
    rownum = 0

    

    for i in range(len(countrylist)):
        if countrylist[i] == country:
            rownum = i
            break
    
    for year in range(endyear-startyear+1):
        #print(float(df.loc[rownum+1][startyear-1990+34+year]))
        newdata.append(float(df.loc[rownum+1][startyear-1990+34+year])-float(df.loc[rownum][startyear-1990+2+year]))
        #newdata += list(df.loc[rownum+1][startyear-1990+2+year]-df.loc[rownum][startyear-1990+28+year]) #Top percentile - bottom 50 percentile for each year to create a new list of data
    #Length of list depend on how many years to show
    #Adding 2 and 34 is for column position offset 

    return newdata
    
def yearrangeChecker(datastartyear, dataendyear, userstartyear, userendyear):
    if datastartyear >userstartyear:
        userstartyear = datastartyear
    if dataendyear < userendyear:
        userendyear = dataendyear
    return userstartyear, userendyear
   
    

file1 = "Data/CrimeRates/brazil-crime-rate-statistics.csv"
file2 = "Data/ConcumerPriceIndex/CPI_IN.xlsx"
file3 = "Data/IncomePolarization/IncomeInequality_World.xls"
#print(cleanIncomedata(file3," Brazil",2000,2010))
#print(cleanCPIdata(file2,1980,2010))
#cleanCSVdata(file1," Brazil",1985,3000)

datalst = cleanCSVdata(file1," Brazil",1985,3000)
cleanCPIdata(file2,1980,2010)
cleanIncomedata(file3," Brazil",2000,2010)

'''
### To work on: ###
allow user to input starting year before the start year in data set but only show start year in data set
for CPI, have some col that have year but no data. be able to check and only start where the data show
'''

df = pd.DataFrame (datalst, columns = ['column_name'])