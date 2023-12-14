# truck class
import heapq
from Classes import packages, ship, dayTime


#  reads the deadline attribute of the package and assigns a number to the attribute,
#  which is used as the priority value. It creates a tuple that is added to the packages list.
def checkDeadline(package):
    if package.deadline == "9:00 AM":
        #  set first priority to 1, then second priority to distance from hub
        return 1, package

    elif package.deadline == "10:30 AM":
        #  set first priority to 2, then second priority to distance from hub
        return 2, package

    else:
        return 3, package


class Truck:

    def __init__(self, truckNumber, packageLimit=16):
        self.truckNumber = truckNumber
        self.remainingPackages = [[], [], []]
        self.deliveredPackages = []
        self.counter = 0

#  this loads packages onto the truck based on the specific requirements of each package.
    def loadPackages(self):
        #  loads packages only allowed on truck2
        if self.truckNumber == 2:
            for j in range(1, 41):
                package = packages.packageList.search(j)
                if "truck 2" in package.notes and "At Hub" in package.status:
                    self.loadSinglePackage(package, j)
                    self.loadLocationDupes(package)

        #  loads packages onto truck
        for i in range(1, 41):
            while self.totalPackages() < 16:
                package = packages.packageList.search(i)

                if "truck 2" in package.notes:
                    break

                if ("Delayed" in package.notes or "Wrong address" in package.notes) and (dayTime.checkTime()):
                    break

                if self.truckNumber != 2 and package.id in (13, 14, 15, 16, 19, 20):
                    break

                if "At Hub" in package.status:
                    self.loadSinglePackage(package, i)
                    self.loadLocationDupes(package)

                break
        return

    #  Loads packages that have the same address of the package in parameters (excluding delayed packages)
    def loadLocationDupes(self, truckPackage):
        for i in range(1, 41):
            if self.totalPackages() == 16:
                return
            package = packages.packageList.search(i)
            if "At Hub" in package.status and not package.notes:
                if ((package.locationIndex == truckPackage.locationIndex) and
                        (("Delayed" not in package.notes) or ("Wrong address" not in package.notes))):
                    self.loadSinglePackage(package, i)

    #  Loads package with a priority of deadlines
    def loadSinglePackage(self, package, i):
        d = checkDeadline(package)
        if d[0] == 1:
            heapq.heappush(self.remainingPackages[0], d)
        elif d[0] == 2:
            heapq.heappush(self.remainingPackages[1], d)
        else:
            heapq.heappush(self.remainingPackages[2], d)

        package.status = "Loaded"
        packages.packageList.insert(i, package)

    def loadPackage(self, package):
        d = checkDeadline(package)
        if d[0] == 1:
            heapq.heappush(self.remainingPackages[0], d)
        elif d[0] == 2:
            heapq.heappush(self.remainingPackages[1], d)
        else:
            heapq.heappush(self.remainingPackages[2], d)

        package.status = "Loaded"
        packages.packageList.insert(package.id, package)

    def printRemainingPackages(self):
        for i in range(0, 3):
            for j in range(len(self.remainingPackages[i])):
                print(self.remainingPackages[i][j][1], sep='\n')

    def printDeliveredPackages(self):
        for i in self.deliveredPackages:
            print(i)

    #  Returns the total number of packages in the truck, which are separated in different lists by package deadline
    def totalPackages(self):
        return len(self.remainingPackages[0]) + len(self.remainingPackages[1]) + len(self.remainingPackages[2])

    #  takes the location index of the last package in the truck and calculates distance from there to the hub.
    #  used to send driver back to hub to load packages
    def returnToHub(self):
        currentLocation = self.deliveredPackages[-1].locationIndex
        distance = ship.getDistance(currentLocation, 0)

        minutes = ship.calculateTime(distance)
        dayTime.time += minutes

        ship.combinedDistance += distance

        return dayTime.time
