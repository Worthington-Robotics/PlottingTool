import csv
import sys
import os
import re
import math
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import filedialog as fd

#Grapher Constants
markerSize = 2
markerStyle = "o"
lineSize = 1
lineStyle = "dashed"
borders = [0.05, 0.98, 0.05, 0.95] #L R B T
whitelistTypes = ["Pose2D", "Twist2D", "Rotation2D", "double", "int", "float", "long", "boolean"]
filteredHeaders = []


window = Tk()
filename = "Example Filepath"
rows = []
headers = []
filename = ""
headerSelector = Listbox(window, height= len(filteredHeaders), width=50, selectmode = EXTENDED)
headerSelector.yview

def selectAllHeaders(*args):
    global headerSelector
    headerSelector.selection_set(0, headerSelector.size())

def headerWhiteListFilter(item: str):
    global whitelistTypes
    for whitelisted in whitelistTypes:
        if "_" + whitelisted == item[item.index("_"):len(item)]:
            return True
    return False

def selectFilePath(*args):
    global rows
    global filteredHeaders
    global headers
    global headerSelector
    global filename
    filename = fd.askopenfilename(title="Select a Robot Data File", initialdir = "Users\Workstation\Documents\GitHub\2021RobotCode\RobotCode\src\main\sim", filetypes=(('Data Files', '*.csv'), ('All Files', '*.*')))
    if not os.path.isfile(filename):
        print("Specifed file could not be found")
        print(filename)
        exit(-1)
    
    #open the file and read it into memory
    print("opening ", filename)
    with open(str(filename)) as csvFile:
        csvReader = csv.reader(csvFile,  delimiter=',')
        rows = [row for row in csvReader]
    if(len(rows) < 1):
        print("File was empty")
        exit(-3)

    pathTextBox = Label(window, text=filename, fg='black', font=("Times New Roman", 11))
    pathTextBox.grid(row=3, column=2)
    
    #filter the headers to find the actual values and no derivatives
    headers = rows[0]
    del rows[0] #remove the header row
    filteredHeaders = [re.sub("_[0-9]","", item) for item in headers]
    filteredHeaders = list(set(filteredHeaders))
    filteredHeaders.remove("time_double")
    filteredHeaders = list(filter(headerWhiteListFilter, filteredHeaders))
    print("got headers:", filteredHeaders)

    #read in optional argument for specific plot
    if(len(sys.argv) == 3):
        toFind = " " + sys.argv[2] 
        if(not toFind in filteredHeaders):
            print("Header '{0}' not found or not valid".format(toFind))
            exit(-4)
        else: 
            filteredHeaders = [toFind]
    
    #Show Chart and allow selection of headers
    
    headerSelector.delete(first=0, last=headerSelector.size())
    for i in range(len(filteredHeaders)):
        headerSelector.insert(END, filteredHeaders[i]) 
    headerSelector.grid(row=2, column=2)
    selectAll = Button(window, text="Select All Commands", command=selectAllHeaders)
    selectAll.grid(row=1,column=3)

    
def remakeListfromKnownFile(*args):
    global rows
    global filteredHeaders
    global headers
    global headerSelector
    global filename
    if not os.path.isfile(filename):
        print("Specifed file could not be found")
        print(filename)
        exit(-1)
    
    #open the file and read it into memory
    print("opening ", filename)
    with open(str(filename)) as csvFile:
        csvReader = csv.reader(csvFile,  delimiter=',')
        rows = [row for row in csvReader]
    if(len(rows) < 1):
        print("File was empty")
        exit(-3)

    pathTextBox = Label(window, text=filename, fg='black', font=("Times New Roman", 11))
    pathTextBox.grid(row=3, column=2)
    
    #filter the headers to find the actual values and no derivatives
    headers = rows[0]
    del rows[0] #remove the header row
    filteredHeaders = [re.sub("_[0-9]","", item) for item in headers]
    filteredHeaders = list(set(filteredHeaders))
    filteredHeaders.remove("time_double")
    filteredHeaders = list(filter(headerWhiteListFilter, filteredHeaders))
    print("got headers:", filteredHeaders)

    #read in optional argument for specific plot
    if(len(sys.argv) == 3):
        toFind = " " + sys.argv[2] 
        if(not toFind in filteredHeaders):
            print("Header '{0}' not found or not valid".format(toFind))
            exit(-4)
        else: 
            filteredHeaders = [toFind]
    
    #Show Chart and allow selection of headers
    
    headerSelector.delete(first=0, last=headerSelector.size())
    for i in range(len(filteredHeaders)):
        headerSelector.insert(END, filteredHeaders[i]) 
    headerSelector.grid(row=2, column=2)
    selectAll = Button(window, text="Select All Commands", command=selectAllHeaders)
    selectAll.grid(row=1,column=3)
    
def headerWhiteListFilter(item: str):
    global whitelistTypes
    for whitelisted in whitelistTypes:
        if "_" + whitelisted == item[item.index("_"):len(item)]:
            return True
    return False

def graph(*args):
    global rows
    global markerSize
    global markerStyle
    global lineSize
    global lineStyle
    global borders
    global filteredHeaders
    global headers
    global headerSelector

    selected = headerSelector.curselection()
    selectedbutalist = list(selected)
    selectedbutalist.sort()

    workingvar = False
    deleted = 0
    for j in range(len(filteredHeaders)):
        workingvar = False
        for selection in selectedbutalist:
            if j==selection:
                workingvar = True
        if not workingvar:
            filteredHeaders.pop(j-deleted)
            deleted += 1        

    #confirm final headers to plot
    filteredHeaders.sort()

    #generate the specific subplots
    width = height = 0
    width = math.ceil(math.sqrt(len(filteredHeaders)))
    if width * (width - 1) >= len(filteredHeaders):
        #print("not square {0} {1} using range {2}".format(width, width - 1, list(range(width - 1, 1, -1))))
        if(width - 1 == 1): 
            #print("using height of 1")
            height = 1
        for heightGuess in range(width - 1, 1, -1):
            #print("guessing {0} {1}".format(width, heightGuess))
            if width * heightGuess >= len(filteredHeaders):
                height = heightGuess
            else: break
    else: height = width 

    #create the plot matrix
    print("Creating {0} by {1} plot matrix".format(width, height))
    fig, axesMat = plt.subplots(height, width)
    if(not type(axesMat) is np.ndarray):
        axes = []
        axes.append(axesMat)
    elif(type(axesMat[0]) is np.ndarray):
        #plot grid is a matrix
        axes = [item for sublist in axesMat for item in sublist]
    else:
        #plot grid is not a matrix
        axes = [item for item in axesMat]

    #print(axes)
    print("using headers:", filteredHeaders)

    #plot the values
    for index in range(len(filteredHeaders)):
        headerGroup = filteredHeaders[index]
        if "_Pose2d" in headerGroup:
            print("Creating pose graph for", headerGroup)
            x = [float(item[headers.index(headerGroup+"_0")]) for item in rows]
            y = [float(item[headers.index(headerGroup+"_1")]) for item in rows]
            axes[index].plot(x, y, color="blue", marker=markerStyle, markersize=markerSize, linestyle=lineStyle, linewidth=lineSize)
            minYVal = min(y)
            maxYVal = max(y) + 1
        elif "_Twist2d" in headerGroup:
            print("Creating twist graph for", headerGroup)
            x = [float(item[headers.index("time_double")]) for item in rows]
            y0 = [float(item[headers.index(headerGroup + "_0")]) for item in rows]
            y1 = [float(item[headers.index(headerGroup + "_1")]) for item in rows]
            y2 = [float(item[headers.index(headerGroup + "_2")]) for item in rows]
            axes[index].plot(x, y0, color="red", marker=markerStyle, markersize=markerSize, linestyle=lineStyle, linewidth=lineSize)
            axes[index].plot(x, y1, color="green", marker=markerStyle, markersize=markerSize, linestyle=lineStyle, linewidth=lineSize)
            axes[index].plot(x, y2, color="blue", marker=markerStyle, markersize=markerSize, linestyle=lineStyle, linewidth=lineSize)
            minYVal = min(min(y0), min(y1), min(y2))
            maxYVal = max(max(y0) + 1, max(y1) + 1, max(y2) + 1)
        elif "_boolean" in headerGroup:
            print("plotting truthy value with time", headerGroup)
            x = [float(item[headers.index("time_double")]) for item in rows]
            y = [int(item[headers.index(headerGroup)] == "true") for item in rows]
            axes[index].plot(x, y, color="blue", marker=markerStyle, markersize=markerSize, linestyle=lineStyle, linewidth=lineSize)
            minYVal = min(y)
            maxYVal = max(y) + 1
        elif "_double[]" in headerGroup:
            print("plotting numeric array")
            #TODO add array type support
        elif "_Rotation2d" in headerGroup:
            print("plotting rotation with time")
            x = [float(item[headers.index("time_double")]) for item in rows]
            y = [float(item[headers.index(headerGroup + "_0")]) for item in rows]
            axes[index].plot(x, y, color="blue", marker=markerStyle, markersize=markerSize, linestyle=lineStyle, linewidth=lineSize)
            minYVal = min(y)
            maxYVal = max(y) + 1
        else:
            print("plotting numeric value with time", headerGroup)
            x = [float(item[headers.index("time_double")]) for item in rows]
            y = [float(item[headers.index(headerGroup)]) for item in rows]
            axes[index].plot(x, y, color="blue", marker=markerStyle, markersize=markerSize, linestyle=lineStyle, linewidth=lineSize)
            minYVal = min(y)
            maxYVal = max(y) + 1

        minXVal = min(x)
        maxXVal = max(x) + 1
        axes[index].set_xticks(np.arange(minXVal, maxXVal, (maxXVal - minXVal) / 10))
        axes[index].set_yticks(np.arange(minYVal, maxYVal, (maxYVal - minYVal) / 10))
        axes[index].set_title(headerGroup.replace("_", " "))
        axes[index].grid(True)

    plt.subplots_adjust(left=borders[0], bottom=borders[2], right=borders[1], top=borders[3])
    plt.show()

# pathTextBoxLabel = Label(window, text="Please Find Path to Robot Data File Here")
pathOpenFileDialogButton = Button(window, text="Please Find Path to Robot Data File Here!", command=selectFilePath)
# pathTextBox = Label(window, text="")
resetlistbutton = Button(window, text="Select me before reselecting graphs to make!", command=remakeListfromKnownFile)
graphButton = Button(window, text="Press me to Graph", command=graph)
graphButton.bind('KeyPress-g', graph)

# pathTextBoxLabel.grid(row=0, column=2)
pathOpenFileDialogButton.grid(row=1, column=2)
resetlistbutton.grid(row=2, column=3)
# pathTextBox.grid(row=2, column=2)
graphButton.grid(row=4, column=2)

window.title("Worbots 4145 Graphing Utility")
window.resizable(width = True, height = True)
window.mainloop()

