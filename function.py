"""
 Function.py contains the functions to clean and parse data from csv, xlsx, json & txt
"""

import pandas as pd

# Clean Crime Rates Data and extract data
def cleanCrimedata(filename,startyear,endyear):
    """
        Clean Crime Rates Data and extract data
        Usage:
            file1 = "data/CrimeRates/"+country.replace(" ","-").lower()+"-crime-rate-statistics.csv"
            print(cleanCrimedata(file1," Brazil",1985,3000))
    """
    df = pd.read_csv(filename,skiprows=16)
    datasetstartyear = int((df["date"][0])[:4])
    datasetendyear = int((df["date"][len(df["date"])-1])[:4])
    #ensure the year range is appropriate for the dataset
    startyear,endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)

    startrow = startyear - datasetstartyear
    print(startrow)
    newdata = []
    yearlist = []
    print(startrow,endyear,startyear)
    
    for year in range(startyear,endyear+1):
        for row in range(len(df["date"])):
            if int(df["date"][startrow+row][:4]) == year:
                newdata.append(round(float(df[" Per 100K Population"][startrow+row]),4))
                yearlist.append(int(year))
            if int(df["date"][startrow+row][:4]) >= year:
                break
        
    dict1 = {"Year":yearlist, 'Crime Rates Per 100k Population':newdata}
    newdf = pd.DataFrame (dict1)
    return newdf


# Clean CPI Data XLSX and extract data
def cleanCPIdata(filename,startyear,endyear):
    """
        Clean CPI Data XLSX and extract data
        Usage:
            file2 = "data/CosumerPriceIndex/CPI_"+convertname(country)+".xlsx"
            print(cleanCPIdata(file2,1980,2010))
    """
    df = pd.read_excel(filename)
    # print(df.loc[1][1]) #starts from column 1 row 4, get value from start of each year so column = 12*n-1, starting from when crime rates starts recording
    newdata = []
    yearlist = []
    datasetstartcol = 0

    # Finds for which col the data starts to show
    for i in range(1,len(df.loc[4])):
        if str(df.loc[4][i]) != 'nan':
            datasetstartcol = i
            break
    
    datasetstartyear = int((df.loc[1][datasetstartcol])[:4])
    datasetstartmonth = int((df.loc[1][datasetstartcol])[-2:])
    datasetendyear = int((df.loc[1][len(df.loc[1])-1])[:4])
    
    startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)
    startcol = datasetstartcol + (13-datasetstartmonth+(startyear-datasetstartyear-1)*12)
    
    # Append data into list
    for year in range(endyear-startyear+1):
        newdata.append(round(float(df.loc[4][startcol+year*12]),2))
        yearlist.append(int(startyear+year))
    dict1 = {"Year":yearlist, 'Consumer Price Index':newdata}
    newdf = pd.DataFrame (dict1) 

    return newdf


# Clean Income Inequality Data XLSX and extract data
def cleanIncomedata(filename,country,startyear,endyear):
    """
        Clean Income Inequality Data XLSX and extract data
        Usage:
            file3 = "data/IncomePolarization/IncomeInequality_World.xls"
            print(cleanIncomedata(file3," Brazil",2000,2010))
    """
    startyear, endyear = int(startyear), int(endyear)
    df = pd.read_excel(filename, sheet_name="Data")
    countrylist = df["Country"]
    newdata = []
    yearlist = []
    rownum = 0
    if country == "United States":
        country = "USA"
    country = " "+country

    if not country in countrylist:
        return pd.DataFrame({})

    for i in range(len(countrylist)):
        if countrylist[i] == country:
            rownum = i
            break
    
    for year in range(endyear-startyear+1):
        newdata.append(round(float(df.loc[rownum+1][startyear-1990+34+year])-float(df.loc[rownum][startyear-1990+2+year]),4))

    #Top percentile - bottom 50 percentile for each year to create a new list of data
    #Length of list depend on how many years to show
    #Adding 2 and 34 is for column position offset 

        yearlist.append(int(startyear+year))
    dict1 = {"Year":yearlist, "Income Inequality":newdata}
    newdf = pd.DataFrame (dict1)

    return newdf


# Clean Enrollment Data CSV
def cleanEnroldata(filename, Country, startyear, endyear):
    """
        Clean Enrollment Data CSV
        Usage:
            file4 = "data/enrollment.csv"
            print(cleanEnroldata(file4,"Brazil" ,2002,2015))
    """
    df = pd.read_csv(filename)
    countrylist = df["Entity"] #List out all country
    newdata = []
    yearlist = []
    rownum = 0
    check = False
    print(Country)
    
    datasetstartyear,datasetendyear = 0,0

    if not Country in countrylist:
        return pd.DataFrame({})

    for i in range(len(countrylist)):
        if countrylist[i] == Country and check == False:
            datasetstartyear = df.loc[i][2]
            rownum = i
            check = True
        if countrylist[i] != Country and check == True:
            datasetendyear = df.loc[i-1][2]
            break

            
    startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)
    

    for year in range(startyear,endyear+1):
        for row in range(len(countrylist)):
            if df.loc[rownum+row][2] == year:
                newdata.append(round(float(df.loc[rownum+row][3]),4))
                yearlist.append(int(year))
                break
    
   
    dict1 = {"Year":yearlist, 'Gross enrolment ratio, secondary, both sexes (%)':newdata}
    newdf = pd.DataFrame (dict1) 

    return newdf


# Clean Poverty Data CSV
def cleanPovertydata(filename, Country, startyear, endyear):
    """
        Clean Poverty Data CSV
        Usage:
            file5 = "data/poverty-explorer.csv"
            print(cleanPovertydata(file5,"Brazil", 2000,2005))
    """
    df = pd.read_csv(filename)
    countrylist = df["Entity"] #List out all country GINI data at GH = 190
    newdata = []
    yearlist = []
    rownum,endrow = 0,0
    check = False

    datasetstartyear,datasetendyear = 0,0

    if not Country in countrylist:
        return pd.DataFrame({})

    for i in range(len(countrylist)):
        if countrylist[i] == Country and check == False:
            datasetstartyear = int(df["survey_year"][i] // 1)
            rownum = i
            check = True
        if countrylist[i] != Country and check == True:
            datasetendyear = int(df["survey_year"][i-1] // 1)
            endrow = i
            break
    
    startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)
    print(startyear)
    for year in range(startyear,endyear+1):
        for row in range(endrow-rownum):
            if int(df["survey_year"][rownum+row]//1) == year:
                
                newdata.append(round(float(df["gini"][rownum+row]),4))
                yearlist.append(int(year))
                

                break

    dict1 = {"Year":yearlist, 'Gini Index':newdata}
    newdf = pd.DataFrame (dict1) 

    return newdf
    

# Clean Family Data CSV
def cleanFamilyData(filename, Country, startyear, endyear):
    """
        Clean Family Data CSV
        Usage:
            file6 = "data/family.csv"
            print(cleanFamilyData(file6, "Brazil",1000,2012))
    """
    df = pd.read_csv(filename)
    countrylist = df["Entity"] #List out all country GINI data at GH = 190
    newdata = []
    yearlist = []
    endrow, rownum = 0, 0
    check = False

    datasetstartyear,datasetendyear = 0,0

    if not Country in countrylist:
        return pd.DataFrame({})

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
                newdata.append(round(float(df["Share of single parent families"][rownum+row]),4))
                yearlist.append(int(year))
                break

    dict1 = {"Year":yearlist, 'Share of single parent families':newdata}
    newdf = pd.DataFrame (dict1) 
    return newdf


# Clean Data in Json file
def cleanJsondata(filename,Country, startyear,endyear):
    """
        Clean Data in Json file
        Usage:
            file7 = "datasets_user/test.json"
            print(cleanJsondata(file7,"Brazil",1995,1999))
    """
    df = (pd.read_json(filename))
    newdf = df["CountryList"][Country]
    datasetstartyear,datasetendyear = int(list(newdf.keys())[0]),int(list(newdf.keys())[-1])
    newdata = []
    yearlist = []
    factor = df["Factor"]
    print(factor)
    startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)
    
    for year in range(startyear,endyear+1):
        if str(year) in list(newdf.keys()):
            newdata.append(newdf[str(year)])
            yearlist.append(year)
    
    dict1 = {"Year":yearlist, str(factor):newdata}
    newdf = pd.DataFrame (dict1)

    return newdf


# Clean csv and txt file type
def cleanCSVTXTdata(filename, Country, startyear, endyear):
    """
        Clean CSV and TXT file type
        Usage:
            # Clean CSV file
            file8 = "datasets_user/test.csv"
            print(cleanCSVdata(file8,"Japan",1995,2000))

            # Clean TXT file
            file9 = "datasets_user/test.txt"
            print(cleanCSVTXTdata(file9,"Mexico",1995,2000))
    """
    df = ""
    if filename[-3:] == "csv":
        df = pd.read_csv(filename)
    elif filename[-3:] == "txt":
        df = pd.read_csv(filename, sep=" ")
    countrylist = df["Country"]
    newdata = []
    yearlist = []
    endrow, rownum = 0, 0
    check = False
    factor = df.columns[2]

    datasetstartyear,datasetendyear = 0,0

    for i in range(len(countrylist)):
        if countrylist[i] == Country and check == False:
            datasetstartyear = int(df["Year"][i])
            rownum = i
            check = True
        if countrylist[i] == Country and check == True:
            datasetendyear = int(df["Year"][i])
            endrow = i
            
    startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)
    print(startyear,datasetendyear)
    for year in range(startyear,endyear+1):
        for row in range(rownum,endrow+1):
            if int(df["Year"][rownum + row]) == year:
                print(df["Year"][rownum+row])
                newdata.append(float(df[factor][rownum+row]))
                yearlist.append(int(year))
                break
    
    dict1 = {"Year":yearlist, factor :newdata}
    newdf = pd.DataFrame (dict1) 
    return newdf


# Checks if data range is within a start and end year
def yearrangeChecker(datastartyear, dataendyear, userstartyear, userendyear):
    """
        Checks if data range is within a start and end year
        Usage:
            startyear, endyear = yearrangeChecker(datasetstartyear,datasetendyear,startyear,endyear)
    """
    if datastartyear >userstartyear:
        userstartyear = datastartyear
    if dataendyear < userendyear:
        userendyear = dataendyear
    return userstartyear, userendyear


# Converts country name to short name
def convertname(Country):
    """
        converts country name to short name
        Usage:
            cname = convertname("Singapore")
    """
    convert_dict = {
        "United States": "USA",
        "Singapore": "SG",
        "Japan":"JP",
        "Brazil":"BZ",
        "Jamaica":"JM",
        "France":"FR",
        "Philippines":"PH",
        "India":"IN",
        "South Africa":"SA",
        "Mexico":"MX"
    }
    return convert_dict[Country]


