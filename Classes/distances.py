#  distance data file
import csv

distanceList = []


# Reads the distance table .csv file for the distance between locations
def loadDistanceData(fileName):
    with open(fileName) as distanceData:
        distances = csv.reader(distanceData, delimiter=',')
        next(distances)  # Skip Header
        for distance in distances:
            distanceList.append(distance)
        fillEmptyDistanceValues()

        for i in range(0, len(distanceList)):
            for j in range(0, len(distanceList)):
                distanceList[i][j] = float(distanceList[i][j])


#  fills the empty elements with the data matrix [i][j] == [j][i]
def fillEmptyDistanceValues():
    for i in range(0, len(distanceList)):
        for j in range(0, len(distanceList)):
            distanceList[i][j] = distanceList[j][i]


def printDistances():
    for i in range(0, len(distanceList)):
        print(distanceList[i])
