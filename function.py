import pandas as pd
import os


#Clean Crime Rates Data and extract data
def cleanCrimedata(filename,country,startyear,endyear):
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

    newdf = pd.DataFrame (newdata, columns = ['Crime Rates Per 100k Population'])
    return newdf

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

    newdf = pd.DataFrame (newdata, columns = ['Consumer Price Index'])

    return newdf

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

    newdf = pd.DataFrame (newdata, columns = ["Income Inequality"])
    return newdf

def cleanJsondata(filename, startyear,endyear):
    df = pd.read_json(filename)
    print(pd.DataFrame(df))

def cleanEnroldata(filename, Country, startyear, endyear):
    df = pd.read_csv(filename)
    countrylist = df["Entity"] #List out all country
    newdata = []
    rownum = 0
    check = False
    
    datasetstartyear,datasetendyear = 0,0

    for i in range(len(countrylist)):
        if countrylist[i] == Country and check == False:
            datasetstartyear = df.loc[i][2]
            check = True
        if countrylist[i] != Country and check == True:
            datasetendyear = df.loc[i-1][2]
            break
            
    startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)
    

    for year in range(startyear,endyear+1):
        for row in range(len(countrylist)):
            if df.loc[rownum+row][2] == year:
                print( df.loc[rownum+row][2])
                newdata.append(float(df.loc[rownum+row][3]))
                break
            
        #newdata += list(df.loc[rownum+1][startyear-1990+2+year]-df.loc[rownum][startyear-1990+28+year]) #Top percentile - bottom 50 percentile for each year to create a new list of data
    #Length of list depend on how many years to show
    #Adding 2 and 34 is for column position offset 
    print(newdata)
    newdf = pd.DataFrame (newdata, columns = ["Income Inequality"])
    return newdf

def cleanPovertydata(filename, Country, startyear, endyear):
    df = pd.read_csv(filename)
    countrylist = df["Entity"] #List out all country GINI data at GH = 190
    newdata = []
    rownum = 0
    check = False

    datasetstartyear,datasetendyear = 0,0

    for i in range(len(countrylist)):
        if countrylist[i] == Country and check == False:
            datasetstartyear = df["survey_year"][i]
            
            check = True
        if countrylist[i] != Country and check == True:
            datasetendyear = df["survey_year"][i-1]
            
            break
    
    startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)

    for year in range(startyear,endyear+1):
        for row in range(len(countrylist)):
            if df["survey_year"][rownum+row] == year:
                
                newdata.append(float(df["gini"][rownum+row]))
                break
    print(newdata)
    newdf = pd.DataFrame(newdata,columns=["Gini Index"])
    return newdf
    
def cleanFamilyData(filename, Country, startyear, endyear):
    df = pd.read_csv(filename)
    countrylist = df["Entity"] #List out all country GINI data at GH = 190
    newdata = []
    endrow, rownum = 0, 0
    check = False

    datasetstartyear,datasetendyear = 0,0

    for i in range(len(countrylist)):
        if countrylist[i] == Country and check == False:
            datasetstartyear = df["Year"][i]
            rownum = i
            check = True
        if countrylist[i] != Country and check == True:
            datasetendyear = df["Year"][i-1]
            endrow = i
            break
    startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)

    for year in range(startyear,endyear+1):
        for row in range(endrow-rownum):
            if df["Year"][rownum + row] == year:
               
                newdata.append(float(df["Share of single parent families"][rownum+row]))
                break
    
    newdf = pd.DataFrame(newdata,columns=["Share of single parent families"])
    return newdf

def yearrangeChecker(datastartyear, dataendyear, userstartyear, userendyear):
    if datastartyear >userstartyear:
        userstartyear = datastartyear
    if dataendyear < userendyear:
        userendyear = dataendyear
    return userstartyear, userendyear
   
    

file1 = "Data/CrimeRates/brazil-crime-rate-statistics.csv"
file2 = "Data/ConcumerPriceIndex/CPI_IN.xlsx"
file3 = "Data/IncomePolarization/IncomeInequality_World.xls"
file4 = "Data/JsonTesting/test.json"
file5 = "Data/enrollment.csv"
file6 = "Data/poverty-explorer.csv"
file7 = "Data/family.csv"
#cleanCrimedata(file1," Brazil",1985,3000)
#cleanCPIdata(file2,1980,2010)
#cleanIncomedata(file3," Brazil",2000,2010)
#cleanJsondata(file4,1990,1992)
#cleanEnroldata(file5,"Brazil" ,1999,3005)
#cleanPovertydata(file6,"Brazil", 2000,2005)
#cleanFamilyData(file7, "Brazil",1000,2012)

