#  keeps track of the time during the route process
from datetime import datetime

startTime = datetime(2023, 11, 27, 8, 00, 00, 00)
time = datetime(2023, 11, 27, 8, 00, 00, 00)
userTime = datetime(2023, 11, 27, 8, 00, 00, 00)


def printTime():
    return time.strftime("%H:%M")


#  Checks if the time is 8:00AM so the loader knows to skip packages that are delayed or have the wrong address
def checkTime():
    if time > startTime:
        return False
    else:
        return True
