import csv

def dataToCSV (file,country,date1,date2):
    """    
    row ={}
    row["country"] = country
    row["starting date"] = date1
    row["end date"] = date2
    print(row)"""
    with open(file,"r",errors = "ignore") as readFile:
        readObject = csv.reader(readFile)
        with open("dataCSV.csv", "w",errors="ignore") as writeFile:
            writeObject = csv.writer(writeFile)
            for column in readObject:
                writeObject.writerow((country,date1,date2))