#!/usr/bin/env python3

import sys
import csv
import os
from datetime import datetime

def main():
    try:
        if (len(sys.argv) != 3):
            print("Error need to input a bird name and age as arg1 and arg2")
            print("e.g. python3 count.py ZF19162 35")
            return
        else:
            name = str(sys.argv[1]) #e.g. ZF19162
            startAge = int(sys.argv[2]) #e.g. 35
            path = "/Users/catharineharris/Desktop/birddataanalysis/" + name + "/"
            #path = getPath()
            if (not os.path.exists(path)):
                print("Error: Path does not exist.")
                return
            #fathersSong = "A"
            fathersSong = getFathersSong()
            quota = 30
            #quota = getQuota()
            #path = "/Users/catharineharris/Desktop/ZF19162/"
        
            #keyPreference = "B"
            #path = getPath()
            #keyPreference = getKeyPreference()
        
            #name = "ZF19162"
            #KPP = Key Press Preference
            mainname = name + "KPP"
            mainoutfile = mainname + ".csv"
            #out files by type
            oneSongExhaustedof = mainname + "OneSongExhausted.csv"
            bothSongsExhaustedof = mainname + "BothSongsExhausted.csv"
            totalDailyKeyCountof = mainname + "TotalDailyKeyCount.csv"
            analysisOF = mainname + "analysis.csv"
        
            analyzeAndLogAllCSVInPath(quota, mainoutfile, oneSongExhaustedof, bothSongsExhaustedof, totalDailyKeyCountof, analysisOF, startAge, fathersSong, path)
            #analyzeOneCSVInPath(quota, path)
    except ValueError:
        print("Age must be entered as an int.")
        return
    except KeyboardInterrupt or EOFError:
        print("Quitting program")
        return

def analyzeAndLogAllCSVInPath(quota, outfile, of1, of2, of3, of4, startAge, fathersSong, path):
    if(os.path.exists(path)):
        os.chdir(path)
        if (os.path.isfile(outfile)):
            yn = getYesNo("This outfile already exists. Do you want to overwrite? (Y/N)")
            if (yn == "N"):
                print("The outfile was NOT overwritten. Printing results...")
                print("---------------------------------------")
                print("Data for all CSV files in " + path)
                print("---------------------------------------")
                ld = os.listdir(path)
                age = startAge
                for f in ld:
                    if (os.path.isfile(f) and isValidFile(f)):
                        print(f)
                        print("Age: " + str(age))
                        analyzeCSV(quota, f)
                        age = age + 1
                        print("***************************************")
                print("---------------------------------------")
                return
            else:
                #clear outfiles
                clearFile(outfile, path)
                clearFile(of1, path)
                clearFile(of2, path)
                clearFile(of3, path)
                clearFile(of4, path)
                print("The outfile was overwritten. Printing results...")
        #writing new outfiles
        configureOutFile(outfile)
        configureOF3(of1)
        configureOF2(of2)
        configureOF2(of3)
        configureOF4(of4)
        print("---------------------------------------")
        print("Data for all CSV files in " + path)
        print("---------------------------------------")
        ld = os.listdir(path)
        age = startAge
        for f in ld:
            if (os.path.isfile(f) and isValidFile(f)):
                print(f)
                print("Age: " + str(age))
                analyzeAndLogCSV(quota, age, f, outfile, of1, of2, of3)
                age = age + 1
                print("***************************************")
        print("---------------------------------------")
        compileAnalysis(fathersSong, of1, of2, of3, of4)
    else:
        print("Error: Path does not exist.")

def analyzeOneCSVInPath(path):
    printCSVFilesInDir(path)
    fileToRead = getFile()
    #fileToRead = "2019-11-13.csv"
    length = len(fileToRead)
    if(os.path.exists(path)):
        os.chdir(path)
        if (os.path.isfile(fileToRead)):
            if(isValidFile(fileToRead)):
                print("---------------------------------------")
                print("Data for " + fileToRead + " in " + path)
                print("---------------------------------------")
                analyzeCSV(fileToRead)
                print("---------------------------------------")
            elif(fileToRead[length-4:] != ".csv"):
                print("Error: Not a CSV file.")
            else:
                print("Error: This is an outfile that cannot be read.")
        else:
            print("Error: File not found.")
    else:
        print("Error: Path does not exist.")


def analyzeCSV(quota, fileToRead):
    length = len(fileToRead)
    date = fileToRead[:length-4]
    #print(date)
    #return
    with open(fileToRead, "r") as csvfile:
        numTimesAPressed = 0
        numTimesBPressed = 0
        songsExhausted = 0
        
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (row["sensor"] == "A"):
                numTimesAPressed += 1
            else:
                numTimesBPressed += 1
            
            if((int(row["num-times-A-played"]) == quota) and (int(row["num-times-B-played"]) != quota)):
                if (songsExhausted == 0):
                    songsExhausted = 1
                    type = "one song playback (A) exhausted"
                    printData(numTimesAPressed, numTimesBPressed, type)
        
            if((int(row["num-times-A-played"]) != quota) and (int(row["num-times-B-played"]) == quota)):
                if (songsExhausted == 0):
                    songsExhausted = 1
                    type = "one song playback (B) exhausted"
                    printData(numTimesAPressed, numTimesBPressed, type)
    
    if((int(row["num-times-A-played"]) == quota) and (int(row["num-times-B-played"]) == quota) and (row["schedule-complete"] == "True")):
        if (songsExhausted == 1):
            songsExhausted = 2
            type = "both songs playback exhausted"
            printData(numTimesAPressed, numTimesBPressed, type)
    if (songsExhausted == 0): #neither song was exhausted
        print("one song playback NOT exhausted\n")
    if (songsExhausted == 1): #both songs were not exhausted
        print("both songs playback NOT exhausted\n")
    type = "total daily key count"
    printData(numTimesAPressed, numTimesBPressed, type)

def analyzeAndLogCSV(quota, age, fileToRead, outfile, of1, of2, of3):
    length = len(fileToRead)
    date = fileToRead[:length-4]
    #print(date)
    #return
    with open(fileToRead, "r") as csvfile:
        numTimesAPressed = 0
        numTimesBPressed = 0
        songsExhausted = 0
        
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (row["sensor"] == "A"):
                numTimesAPressed += 1
            else:
                numTimesBPressed += 1
            
            if((int(row["num-times-A-played"]) == quota) and (int(row["num-times-B-played"]) != quota)):
                if (songsExhausted == 0):
                    songsExhausted = 1
                    type = "one song playback (A) exhausted"
                    printAndLogData(numTimesAPressed, numTimesBPressed, type, date, age, outfile, of1, of2, of3)
        
            if((int(row["num-times-A-played"]) != quota) and (int(row["num-times-B-played"]) == quota)):
                if (songsExhausted == 0):
                    songsExhausted = 1
                    type = "one song playback (B) exhausted"
                    printAndLogData(numTimesAPressed, numTimesBPressed, type, date, age, outfile, of1, of2, of3)
                        
            if((int(row["num-times-A-played"]) == quota) and (int(row["num-times-B-played"]) == quota) and (row["schedule-complete"] == "True")):
                if (songsExhausted == 1):
                    songsExhausted = 2
                    type = "both songs playback exhausted"
                    printAndLogData(numTimesAPressed, numTimesBPressed, type, date, age, outfile, of1, of2, of3)
    if (songsExhausted == 0): #neither song was exhausted
        type = "one song playback NOT exhausted"
        printAndLogData("NA", "NA", type, date, age, outfile, of1, of2, of3)
        type = "both songs playback NOT exhausted"
        printAndLogData("NA", "NA", type, date, age, outfile, of1, of2, of3)
    if (songsExhausted == 1): #both songs were not exhausted
        type = "both songs playback NOT exhausted"
        printAndLogData("NA", "NA", type, date, age, outfile, of1, of2, of3)
    type = "total daily key count"
    printAndLogData(numTimesAPressed, numTimesBPressed, type, date, age, outfile, of1, of2, of3)

def configureOutFile(outfile):
    with open(outfile, "a") as lf:
        fieldnames = ["Date", "Age", "Type", "numTimesAPressed", "numTimesBPressed", "SumOfBothKeys", "KeyAPreference", "KeyBPreference"]
        writer = csv.DictWriter(lf, fieldnames)
        writer.writeheader()

def configureOF2(outfile):
    with open(outfile, "a") as lf:
        fieldnames = ["Date", "Age", "numTimesAPressed", "numTimesBPressed", "SumOfBothKeys", "KeyAPreference", "KeyBPreference"]
        writer = csv.DictWriter(lf, fieldnames)
        writer.writeheader()

def configureOF3(outfile):
    with open(outfile, "a") as lf:
        fieldnames = ["Date", "Age", "SongExhaustedFirst", "numTimesAPressed", "numTimesBPressed", "SumOfBothKeys", "KeyAPreference", "KeyBPreference"]
        writer = csv.DictWriter(lf, fieldnames)
        writer.writeheader()

##########
#OSE = one song exhausted
#BSE = both songs exhausted
#TDKC = total daily key count
#FS = Fathers Song
#NS = Neighbors Song
##########
def configureOF4(outfile):
    with open(outfile, "a") as lf:
        fieldnames = ["Age", "OSE-FS-Preference", "OSE-NS-Preference", "BSE-FS-Preference", "BSE-NS-Preference", "TDKC-FS-Preference", "TDKC-NS-Preference"]
        writer = csv.DictWriter(lf, fieldnames)
        writer.writeheader()
#########

def logData(outfile, date, age, type, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB):
    with open(outfile, "a") as lf:
        writer = csv.DictWriter(lf, fieldnames = ["Date", "Age", "Type", "numTimesAPressed", "numTimesBPressed", "SumOfBothKeys", "KeyAPreference", "KeyBPreference"])
        writer.writerow(
            {
                "Date": date,
                "Age" : age,
                "Type": type,
                "numTimesAPressed": numTimesAPressed,
                "numTimesBPressed": numTimesBPressed,
                "SumOfBothKeys": sum,
                "KeyAPreference": preferenceForKeyA,
                "KeyBPreference": preferenceForKeyB
            }
        )

def logData2(outfile, date, age, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB):
    with open(outfile, "a") as lf:
        writer = csv.DictWriter(lf, fieldnames = ["Date", "Age", "numTimesAPressed", "numTimesBPressed", "SumOfBothKeys", "KeyAPreference", "KeyBPreference"])
        writer.writerow(
            {
                "Date": date,
                "Age" : age,
                "numTimesAPressed": numTimesAPressed,
                "numTimesBPressed": numTimesBPressed,
                "SumOfBothKeys": sum,
                "KeyAPreference": preferenceForKeyA,
                "KeyBPreference": preferenceForKeyB
            }
        )

def logData3(outfile, date, age, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB, songExhaustedFirst):
    with open(outfile, "a") as lf:
        writer = csv.DictWriter(lf, fieldnames = ["Date", "Age", "SongExhaustedFirst", "numTimesAPressed", "numTimesBPressed", "SumOfBothKeys", "KeyAPreference", "KeyBPreference"])
        writer.writerow(
            {
                "Date": date,
                "Age" : age,
                "SongExhaustedFirst": songExhaustedFirst,
                "numTimesAPressed": numTimesAPressed,
                "numTimesBPressed": numTimesBPressed,
                "SumOfBothKeys": sum,
                "KeyAPreference": preferenceForKeyA,
                "KeyBPreference": preferenceForKeyB
            }
        )

######
def compileAnalysis(fathersSong, of1, of2, of3, of4):
    age = []
    OSEFSPreference = []
    OSENSPreference = []
    BSEFSPreference = []
    BSENSPreference = []
    TDKCFSPreference = []
    TDKCNSPreference = []
    
    with open(of1, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            age.append(row["Age"])
            if (fathersSong == "A"):
                OSEFSPreference.append(row["KeyAPreference"])
                #OSENSPreference.append(row["KeyBPreference"])
                if (row["KeyBPreference"] != "NA"):
                    OSENSPreference.append(-1*float(row["KeyBPreference"]))
                else:
                    OSENSPreference.append(row["KeyBPreference"])
            else:
                if (row["KeyAPreference"] != "NA"):
                    OSENSPreference.append(-1*float(row["KeyAPreference"]))
                else:
                    OSENSPreference.append(row["KeyAPreference"])
                #OSENSPreference.append(row["KeyAPreference"])
                OSEFSPreference.append(row["KeyBPreference"])

    with open(of2, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (fathersSong == "A"):
                BSEFSPreference.append(row["KeyAPreference"])
                #BSENSPreference.append(row["KeyBPreference"])
                if (row["KeyBPreference"] != "NA"):
                    BSENSPreference.append(-1*float(row["KeyBPreference"]))
                else:
                    BSENSPreference.append(row["KeyBPreference"])
            else:
                #BSENSPreference.append(row["KeyAPreference"])
                if (row["KeyAPreference"] != "NA"):
                    BSENSPreference.append(-1*float(row["KeyAPreference"]))
                else:
                    BSENSPreference.append(row["KeyAPreference"])
                BSEFSPreference.append(row["KeyBPreference"])

    with open(of3, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (fathersSong == "A"):
                TDKCFSPreference.append(row["KeyAPreference"])
                #TDKCNSPreference.append(row["KeyBPreference"])
                if (row["KeyBPreference"] != "NA"):
                    TDKCNSPreference.append(-1*float(row["KeyBPreference"]))
                else:
                    TDKCNSPreference.append(row["KeyBPreference"])
            else:
                #TDKCNSPreference.append(row["KeyAPreference"])
                if (row["KeyAPreference"] != "NA"):
                    TDKCNSPreference.append(-1*float(row["KeyAPreference"]))
                else:
                    TDKCNSPreference.append(row["KeyAPreference"])
                TDKCFSPreference.append(row["KeyBPreference"])

    numEntries = len(age)
    n = 0
    while(n < numEntries):
        with open(of4, "a") as f:
            writer = csv.DictWriter(f, fieldnames = ["Age", "OSE-FS-Preference", "OSE-NS-Preference", "BSE-FS-Preference", "BSE-NS-Preference", "TDKC-FS-Preference", "TDKC-NS-Preference"])
            writer.writerow(
                {
                    "Age" : age[n],
                    "OSE-FS-Preference": OSEFSPreference[n],
                    "OSE-NS-Preference": OSENSPreference[n],
                    "BSE-FS-Preference": BSEFSPreference[n],
                    "BSE-NS-Preference": BSENSPreference[n],
                    "TDKC-FS-Preference": TDKCFSPreference[n],
                    "TDKC-NS-Preference": TDKCNSPreference[n]
            }
        )
        n=n+1

######

def printAndLogData(numTimesAPressed, numTimesBPressed, type, date, age, outfile, of1, of2, of3):
    if (type != "total daily key count" and type != "one song playback NOT exhausted" and type != "both songs playback NOT exhausted"):
        print("num times A and B pressed when " + type)
    elif(type == "one song playback NOT exhausted"):
        print("one song playback NOT exhausted\n")
    elif(type == "both songs playback NOT exhausted"):
        print("both songs playback NOT exhausted\n")
    else:
        print("num times A and B pressed at end of day")
    if(type != "one song playback NOT exhausted" and type != "both songs playback NOT exhausted"):
        print("A: " + str(numTimesAPressed))
        print("B: " + str(numTimesBPressed))
        sum = numTimesAPressed + numTimesBPressed
        print("Sum of both keys: " + str(sum))
    else:
        sum = "NA"
    preferenceForKey = 0
    if (sum != "NA" and sum != 0):
        #if(keyPreference == "A"):
        preferenceForKeyA = numTimesAPressed/sum
        #else: #keyPreference == "B"
        preferenceForKeyB = numTimesBPressed/sum
        print("Key A preference: " + str(preferenceForKeyA))
        print("Key B preference: " + str(preferenceForKeyB) + "\n")
    else:
        preferenceForKeyA = "NA"
        preferenceForKeyB = "NA"
    logData(outfile, date, age, type, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB)
    if (type == "one song playback (A) exhausted"):
        logData3(of1, date, age, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB, "A")
    elif(type == "one song playback (B) exhausted"):
        logData3(of1, date, age, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB, "B")
    elif(type == "one song playback NOT exhausted"):
        logData3(of1, date, age, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB, "NA")
    elif(type == "both songs playback exhausted"):
        logData2(of2, date, age, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB)
    elif(type == "both songs playback NOT exhausted"):
        logData2(of2, date, age, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB)
    else: #type == "total daily key count"
        logData2(of3, date, age, numTimesAPressed, numTimesBPressed, sum, preferenceForKeyA, preferenceForKeyB)

def printData(numTimesAPressed, numTimesBPressed, type):
    if (type != "total daily key count"):
        print("num times A and B pressed when " + type)
    else:
        print("num times A and B pressed at end of day")
    print("A: " + str(numTimesAPressed))
    print("B: " + str(numTimesBPressed))
    sum = numTimesAPressed + numTimesBPressed
    print("Sum of both keys: " + str(sum))
    #preferenceForKey = 0
    #if(keyPreference == "A"):
    preferenceForKey = numTimesAPressed/sum
    print("Key A preference: " + str(preferenceForKey) + "\n")
    #else: #keyPreference == "B"
    preferenceForKey = numTimesBPressed/sum
    print("Key B preference: " + str(preferenceForKey) + "\n")

def clearFile(filename, path):
    os.chdir(path)
    with open(filename, "w"):
        pass

def test():
    d = "2019-11-01.csv"
    #d = "log.csv"
    #d = "log.txt"
    length = len(d)
    if (d[length-4:] == ".csv"): #check file extension first
        date = d[:length-4]
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            print("Is a valid date " + str(dt))
        except ValueError:
            print("Not a date")
    else:
        print("Not a valid file")
    #############
    #path = "/Users/catharineharris/Desktop/bird1/"
    #os.chdir(path)
    #clearFile("t.txt", path)

def isValidFile(str):
    length = len(str)
    if (str[length-4:] == ".csv"): #check file extension first
        s = str[:length-4] #remove file extension
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    else:
        return False

def getPath():
    print("Please enter the directory path where the data file(s) to analyze are located:")
    print("e.g. /home/pi/Desktop/singsparrow/data/ZF19162/")
    while(True):
        path = input()
        if (not os.path.exists(path)): #path not found
            print("Error: Path not found. Enter a valid path:")
        else:
            return path
               
def getFile():
    print("Please enter the file you wish to read:")
    while(True):
        fileToRead = input()
        if (os.path.isfile(fileToRead)): #file found
            length = len(fileToRead)
            if(isValidFile(fileToRead)):
                return fileToRead
            elif(fileToRead[length-4:] != ".csv"):
                print("Error: Not a CSV file. Enter a valid filename:")
            else: #fileToRead == outfile
                print("Error: This is an outfile that cannot be read. Enter a valid filename:")
        else: #file not found
            print("Error: File not found. Enter a valid filename:")

"""
def getKeyPreference():
    print("Please enter your key preference (A or B):")
    while(True):
        key = input()
        if (key == "A" or key == "a"):
            return "A"
        elif(key == "B" or key == "b"):
            return "B"
        else:
            print("Error: invalid input. Enter a valid key preference (A or B):")
"""
               
def printCSVFilesInDir(path):
    if(os.path.exists(path)):
        os.chdir(path)
        print("\nCSV files in " + path)
        print("---------------------------------------")
        ld = os.listdir(path)
        for f in ld:
            if (os.path.isfile(f) and isValidFile(f)):
                print(f)
                """
                length = len(f)
                if(f[length-4:] == ".csv"):
                    print(f)
                """
        print("---------------------------------------")

def getQuota():
    while(True):
        key = input("Enter the quota number: ")
        try:
            return int(key)
        except TypeError and ValueError:
            print("Error: not an integer.")


def getFathersSong():
    while(True):
        key = input("Enter the key associated with the father's song (A/B): ")
        if (key == "A" or key == "a"):
            return "A"
        elif (key == "B" or key == "b"):
            return "B"
        else:
            print("Error: invalid input.")


def getYesNo(text):
    print(text)
    while(True):
        key = input()
        if (key == "Y" or key == "y" or key == "yes" or key == "YES"):
            return "Y"
        elif(key == "N" or key == "n" or key == "no" or key == "NO"):
            return "N"
        else:
            print("Error: invalid input. Enter Y/N:")

#test()
main()
