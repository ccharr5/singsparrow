#!/usr/bin/env python3

import os
import sys
import csv
import matplotlib.pyplot as plt

def main():
    try:
        if (len(sys.argv) != 2):
            print("Error need to input a bird name as arg1")
            print("e.g. python3 graph.py ZF19162")
            return
        else:
            name = str(sys.argv[1])
            path = "/Users/catharineharris/Desktop/birddataanalysis/" + name + "/"
            #path = getPath()
            if (not os.path.exists(path)):
                print("Error: Path does not exist.")
                return
            os.chdir(path)
            analysisOF = name + "KPPanalysis.csv"
            if (not os.path.isfile(analysisOF)):
                print("Error: File to graph does not exist.")
                return
            
            graph(analysisOF, name+"OSE.png", name + " One Song Exhausted", 1, 2)
            graph(analysisOF, name+"BSE.png", name + " Both Songs Exhausted", 3, 4)
            graph(analysisOF, name+"TDKC.png", name + " Total Daily Key Count", 5, 6)
            """
            graph2(analysisOF, name + " One Song Exhausted", 1, 2)
            graph2(analysisOF, name + " Both Songs Exhausted", 3, 4)
            graph2(analysisOF, name + " Total Daily Key Count", 5, 6)
            """
    except KeyboardInterrupt or EOFError:
        print("Quitting program")
        return

def graph(file, t1, title, c1, c2):
    x = []
    fs = []
    ns = []
    
    with open(file, "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        z = 0
        for row in plots:
            if (z != 0):
                x.append(int(row[0]))
                if(row[c1] != "NA"):
                    fs.append(float(row[c1]))
                else:
                    fs.append(0)
                if(row[c2] != "NA"):
                    ns.append(float(row[c2]))
                else:
                    ns.append(0)
            z = 1
    """
    print(x)
    print(fs)
    print(ns)
    """
    
    p1 = plt.bar(x, fs)
    p2 = plt.bar(x, ns)
    #plt.xticks(x)
    plt.xticks(x, x, fontsize=5, rotation=90)

    plt.title(title)
    plt.legend((p1[0], p2[0]), ("Father's Song", "Neighbor's Song"))
    plt.xticks(x)
    plt.xlabel("Age (days)")
    plt.ylabel("Preference (%)")

    #plt.show()
    plt.savefig(t1)
    plt.close()
    #plt.savefig(t1+".png")
    #savefig('foo.png', bbox_inches='tight')

def graph2(file, title, c1, c2):
    x = []
    fs = []
    ns = []
    
    with open(file, "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        z = 0
        for row in plots:
            if (z != 0): #skip headers
                if(row[c1] != "NA" or row[c2] != "NA"):
                    x.append(int(row[0]))
                if(row[c1] != "NA" and row[c2] != "NA"):
                    fs.append(float(row[c1]))
                    ns.append(float(row[c2]))
                elif(row[c1] != "NA"):
                    fs.append(float(row[c1]))
                    ns.append(0)
                elif(row[c2] != "NA"):
                    fs.append(0)
                    ns.append(float(row[c2]))
                else:
                    pass
            z = 1
        """
            print(x)
            print(fs)
            print(ns)
            """
    if (x != [] and fs != [] and ns != 0):
        p1 = plt.bar(x, fs)
        p2 = plt.bar(x, ns)
        plt.xticks(x)
        
        plt.title(title)
        plt.legend((p1[0], p2[0]), ("Father's Song", "Neighbor's Song"))
        plt.xticks(x)
        plt.xlabel("Age (days)")
        plt.ylabel("Preference (%)")
        
        plt.show()
        
def getPath():
    print("Please enter the directory path where the data file(s) to analyze are located:")
    print("e.g. /home/pi/Desktop/singsparrow/data/ZF19162/")
    while(True):
        path = input()
        if (not os.path.exists(path)): #path not found
            print("Error: Path not found. Enter a valid path:")
        else:
            return path

main()
