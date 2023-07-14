""" Trying to convert csv file to Sumo calibrators in xml
Param 1: path to csv file that contains the flow rate in vehicles per hour 
Param 2: Sampling rate at which the data was taken
Param 3: Name of generated file. Program will append '.add.xml' to the name. Default is 'importCalibData.add.xml'.

May add more functionality in the future

Coded for versions of Python 3 and above

Author: Phillip Chen 11/2022
"""

import csv
import sys
import argparse
import xml.etree.ElementTree as ET
import xml.dom.minidom


# Creating argparser object
argparser = argparse.ArgumentParser(description='Generates an xml file for Sumo calibrators that will control'+ 
    'the flow of vehicles (int vehs/hr) over each edge of the Carla simulation based on the given csv file' +
    "Takes in an output file name, default 'importCalibData' ")

argparser.add_argument(
    '-f', '--file',
    metavar='File',
    required=True,
    type=str,
    dest='fileName',
    help="Input CSV file"
)

argparser.add_argument(
    '-r', '--rate',
    metavar='Sampling Rate',
    required=True,
    type=int,
    dest='sample_rate',
    help="The rate of which data values are taken in seconds. Converted to integers"
)

argparser.add_argument(
    '-n', '--name',
    metavar='Output File',
    default="importCalibData",
    type=str,
    dest='outputFile',
    help="The name of the outputted xml file. Do not include '.add.xml', that will be automatically appended. Default name is 'importCalibData'"
)

# Error message if an incorrect amount of inputs are given
if len(sys.argv) < 2:
    argparser.print_help()
    exit

# Parsing arguments
args = argparser.parse_args()
fileName = args.fileName
sampleRate = args.sample_rate
outputFileName = args.outputFile + ".add.xml"

"""
 Will store the data as a dictionarys.
 The keys are the start of the time intervals
 The values are the flow rate (float) over that time interval
 The time intervals between flow rates will be the from the start time of one to the start time of the other.
"""
data = {}

currTime = 0

with open(fileName) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    lineCount = 0

    for row in csv_reader:
        if ("," in row):
            raise("CSV file should only have a single column of data")
            exit
        else:
            flowRate= float(row[0])
            data[currTime] = flowRate
            currTime+= sampleRate
            lineCount+=1
    print(f"Processed {lineCount} lines.")

# Label for the Sumo Edges in Gomentum
sumoEdges = ["-24", "-11", "-0", "5", "6"]# "12", "13", "15", "16", "21" "22"] # Removed 4, 14, 3, and 25 because of performance issues

""" 
The following creates the xml file.
"""
# This file is an additional file
root = ET.Element("additional")

# Adding routes and calibrators
for i in range(len(sumoEdges)):
    # Creating Routes
    route = ET.Element("route")
    route.set('edges', sumoEdges[i])
    route.set('id', "r_" + str(i))
    root.append(route)

    # Creating Calibrator
    calibrator = ET.Element("calibrator")
    calibrator.set("pos", "0.00")
    calibrator.set("id", "ca_" + str(i))
    calibrator.set("edge", sumoEdges[i])
    root.append(calibrator)

    # Creating Flows
    for time in data.keys():
        flow = ET.SubElement(calibrator, "flow")
        flow.set("vehsPerHour", str(data[time]))
        flow.set("route", "r_" + str(i))
        flow.set("begin", str(time))
        flow.set("end", str(time + sampleRate))
        flow.set("type", "DEFAULT_VEHTYPE")
        
# Creating xml tree
tree = ET.ElementTree(root)
tree = xml.dom.minidom.parseString(ET.tostring(tree.getroot())).toprettyxml(indent="    ")

# Creating and writing to file
with open(outputFileName, "w") as files:
    files.write(tree)

print("Successfully created " + outputFileName)