from datetime import datetime, timedelta

from Classes import distances, dayTime, packages

combinedDistance = 0.0
truckDistance = 0.0


#  This starts the algorithms for shipping each package, calculating the distance for the nearest-neighbor.
def startRoute(truck):
    #  resets time for each truck to get an accurate delivery time, unless it's truck number 3
    if truck.truckNumber != 3:
        dayTime.time = datetime(2023, 11, 27, 8, 00, 00, 00)

    #  checks if each deadline list has any elements; if it does, begins closest package from hub
    if truck.remainingPackages[0]:
        prevLocationIndex = findDistanceFromHub(truck, truck.remainingPackages[0])

    elif truck.remainingPackages[1]:
        prevLocationIndex = findDistanceFromHub(truck, truck.remainingPackages[1])

    else:
        prevLocationIndex = findDistanceFromHub(truck, truck.remainingPackages[2])

    #  for each deadline, ships each package
    for packageList in truck.remainingPackages:
        if packageList:
            shipPackages(truck, packageList, prevLocationIndex)

    #  combined truck distance
    global combinedDistance
    combinedDistance += truckDistance


def getDistance(start, end):
    return distances.distanceList[start][end]


#  this sets the minimum distance of all remaining locations, adds to the total distance travelled, adds to the time,
#  updates the hashtable, and deletes it from the truck's packages. This creates the starting point for the route.
def findDistanceFromHub(truck, truckPackages):
    minPackageIndex = 0
    p = truckPackages[0]
    #  Assigns a starting point for the minimum distance; the first package location
    minDistance = getDistance(0, p[1].locationIndex)

    for i in range(1, len(truckPackages)):
        currentDistance = getDistance(0, truckPackages[i][1].locationIndex)

        if currentDistance < minDistance:
            minDistance = currentDistance
            minPackageIndex = i

    #  Add truck and combined distances to global variable
    global truckDistance
    truckDistance = 0
    truckDistance += minDistance

    #  calculates time and adds time to the master time
    minutes = calculateTime(minDistance)
    dayTime.time += minutes
    if dayTime.time >= dayTime.userTime:
        return

    #  updates hashtable
    truckPackages[minPackageIndex][1].timeDelivered = dayTime.time
    truckPackages[minPackageIndex][1].status = "Delivered"
    packages.packageList.insert(p[1].id, p[1])

    p = truckPackages[minPackageIndex][1]

    truck.deliveredPackages.append(truckPackages[minPackageIndex][1])
    del truckPackages[minPackageIndex]

    return p


#  unloads packages from the truck. This sets the minimum distance of all remaining locations, adds to the total
#  distance travelled, adds to the time, updates the hashtable, and deletes it from the truck's packages. It calls
#  itself to repeat until all packages are gone.
def shipPackages(truck, truckPackages, prevLocation):
    #  Loads packages 25, 31, and 6
    if dayTime.time >= datetime(2023, 11, 27, 9, 00, 00, 00) \
            and truck.truckNumber == 1 and truck.counter == 0:
        truck.returnToHub()
        one = packages.packageList.search(25)
        two = packages.packageList.search(31)
        three = packages.packageList.search(6)
        truck.loadPackage(one)
        truck.loadPackage(two)
        truck.loadPackage(three)
        truck.counter = 1

        shipPackages(truck, truck.remainingPackages[1], prevLocation)

    minLocation = truckPackages[0][1]
    minPackageIndex = 0
    p = truckPackages[0]
    #  Assigns a starting point for the minimum distance; the first package location
    if prevLocation:
        minDistance = getDistance(prevLocation.locationIndex, p[1].locationIndex)
    else:
        return

    deliverSamePackages(truck, prevLocation)

    #  fixes an index-out-of-bound error with the  deliverSamePackages() function; it deletes an item in the list.
    #  If it was the last item in the list, it deletes it then tries to search through an empty list, throwing an error.
    if not truckPackages:
        return

    #  minimum distance calculator
    for i in range(1, len(truckPackages)):
        p = truckPackages[i]
        currentDistance = getDistance(prevLocation.locationIndex, p[1].locationIndex)

        if currentDistance < minDistance:
            minDistance = currentDistance
            minLocation = p[1]
            minPackageIndex = i

    #  Add truck and combined distances to global variable
    global truckDistance
    truckDistance += minDistance

    #  calculates time and adds time to the master time
    minutes = calculateTime(minDistance)
    dayTime.time = dayTime.time + minutes
    if dayTime.time >= dayTime.userTime:
        return

    #  updates hashtable
    truckPackages[minPackageIndex][1].timeDelivered = dayTime.time
    truckPackages[minPackageIndex][1].status = "Delivered"
    packages.packageList.insert(truckPackages[minPackageIndex][1].id,
                                truckPackages[minPackageIndex][1])

    truck.deliveredPackages.append(truckPackages[minPackageIndex][1])
    del truckPackages[minPackageIndex]

    #  recursive
    if truckPackages:
        shipPackages(truck, truckPackages, minLocation)


#  calculates time given distance
def calculateTime(distance):
    t = (distance / 18) * 60
    return timedelta(minutes=t)


# shows the path the truck takes and at what time it gets delivered
def printPath(address):
    print(f"-->  {address}  |  Delivered at: {dayTime.printTime()}  ", sep='\n')


#  searches the truck packages for any other package that needs to be delivered to the current location.
#  the [1] part of the object is the [1] index of a tuple at [i][j].
def deliverSamePackages(truck, currentLocation):
    for i in range(0, 3):
        for j in range(len(truck.remainingPackages[i])):
            if truck.remainingPackages[i]:
                if (truck.remainingPackages[i][j][1].locationIndex == currentLocation.locationIndex and
                        (truck.remainingPackages[i][j][1].id != currentLocation.id)):
                    truck.remainingPackages[i][j][1].timeDelivered = dayTime.time
                    truck.remainingPackages[i][j][1].status = "Delivered"
                    packages.packageList.insert(truck.remainingPackages[i][j][1].id, truck.remainingPackages[i][j][1])
                    truck.deliveredPackages.append(truck.remainingPackages[i][j][1])
                    del truck.remainingPackages[i][j]
                    return
