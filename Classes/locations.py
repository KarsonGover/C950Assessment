# locations data file
import csv

locationList = []


# Reads the address table .csv file for the address name
def loadLocationData(fileName):
    with open(fileName) as locationData:
        locations = csv.reader(locationData)
        next(locations)  # Skip Header
        for location in locations:
            locationList.append(location[0])

        return locationList


def printLocations():
    print(locationList)
