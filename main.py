#  Karson Gover's WGUPS package delivery program - Student ID #002142506
from datetime import datetime

from Classes import packages, locations, distances, ship, dayTime
from Classes.trucks import Truck

# Loads .csv file data
locations.loadLocationData("CSVs/WGUPS Address Table.csv")
distances.loadDistanceData("CSVs/WGUPS Distance Values.csv")
packages.loadPackageData("CSVs/WGUPS Packages.csv")

#  Create truck objects
truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)

#  Load trucks 1 & 2 with packages
truck1.loadPackages()
truck2.loadPackages()


def beginInteraction():
    print("---\n\nWelcome to the WGU Postal Service Dashboard.\n\n---\n")
    userInput = input("To view the progress of the routes, reply with 'routes'. "
                      "\nTo exit the program, reply with 'exit'\n\n---\n\n")
    greetingResponse(userInput)


def greetingResponse(userInput):
    match userInput:
        case "routes":
            userInput = input("\n---\n\nAt what time (in military time) would you like to see the progress"
                              " of the routes? {Example: '10:00' or '17:00'}\n\n---\n\n")

            time = userInput.split(":")
            printPackagesAtTime(time)

        case "exit":
            print("\n---\n\nProgram terminating...")
            exit()

        case _:
            userInput = input("\n---\n\nI'm sorry, that isn't a valid command. "
                              "Please reply with a correct command.\n\n---\n\n")
            greetingResponse(userInput)


#  loads/starts routes of the trucks
def startRoutes():
    truck1.loadPackages()
    truck2.loadPackages()

    #  start trucks 1 & 2 routes
    ship.startRoute(truck1)

    #  returns to hub to load packages onto truck 3
    truck3StartTime = truck1.returnToHub()
    ship.startRoute(truck2)

    #  truck3 leaves when truck1 gets back to hub
    dayTime.time = truck3StartTime

    #  checks if time is 10:20 so package 9 can be updated with the correct address
    if dayTime.time >= datetime(2023, 11, 27, 10, 20, 00, 00):
        package = packages.packageList.search(9)
        package.address = '410 S State St'
        package.zipcode = '84111'
        package.notes = 'Address has been updated.'
        packages.packageList.insert(9, package)

        truck3.loadPackages()
        ship.startRoute(truck3)


#  prints packages at the user's specified time
def printPackagesAtTime(time):
    dayTime.userTime = datetime(2023, 11, 27, int(time[0]), int(time[1]), 00, 00)

    startRoutes()

    print(f"\n---\n\nAt {dayTime.userTime}, here is the progress of the truck routes:")

    print("\n---\n\nPackages at HUB:")

    for i in range(1, 41):
        p = packages.packageList.search(i)
        if p.status == "At Hub":
            print(p)

    print("\n---\n\nTruck 1:")
    print("\n---\n\nRemaining Packages:")
    truck1.printRemainingPackages()
    print("\n\nDelivered Packages:")
    truck1.printDeliveredPackages()

    print("\n---\n\nTruck 2:")
    print("\n---\n\nRemaining Packages:")
    truck2.printRemainingPackages()
    print("\n\nDelivered Packages:")
    truck2.printDeliveredPackages()

    print("\n---\n\nTruck 3:")
    print("\n---\n\nRemaining Packages:")
    truck3.printRemainingPackages()
    print("\n\nDelivered Packages:")
    truck3.printDeliveredPackages()

    print("\n---\n\nCombined Truck Distance:")
    print(f"\n\n{ship.combinedDistance}\n\n")


beginInteraction()
