# package class
import csv
import packageHash
from Classes import locations
from datetime import time

packageList = packageHash.ChainingHashTable()


def loadPackageData(fileName):
    with open(fileName) as packageData:
        packages = csv.reader(packageData, delimiter=',')
        next(packages)  # Skip Header
        for package in packages:
            id = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline = package[5]
            weight = package[6]
            status = "At Hub"
            notes = package[7]

            if address in locations.locationList:
                locationIndex = locations.locationList.index(address)

            package = Package(id, locationIndex, address, city, state, zipcode, deadline, weight, status, notes)

            packageList.insert(id, package)


def printPackageList():
    for package in packageList.table:
        print(package)


class Package:

    def __init__(self, id, locationIndex, address, city, state, zipcode, deadline, weight, status,
                 notes):
        self.id = id
        self.locationIndex = locationIndex
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.timeDelivered = time(0, 0)
        self.weight = weight
        self.status = status
        self.notes = notes

    def __repr__(self):
        return ("ID: %s, Location Index: %s, Address: %s, City: %s, State: %s, Zipcode: %s, Deadline: %s, "
                "Time Delivered: %s, Weight: %s, Status: %s, Notes: %s" %
                (self.id, self.locationIndex, self.address, self.city, self.state, self.zipcode, self.deadline,
                 self.timeDelivered, self.weight, self.status, self.notes))

    #  allows for the comparison of packages
    def __lt__(self, other):
        return self.deadline < other.deadline
