# Waiting
# Code for timed events

from datetime import datetime, time, timedelta
from time import sleep
import json as j

from accounts import findStorage

# Global running data
RUNNING = False
RUNAT = []

# Toggle whether the bot is running
def toggleRunning():
    global RUNNING
    RUNNING = not RUNNING

# Get whether the bot is running
def getRunning():
    global RUNNING
    return RUNNING

# Get the times the code should run at 
def getRunAt():
    global RUNAT
    return RUNAT

# Check if the bot is set to run at the given time
def checkRunTime(runTime):
    global RUNAT
    return runTime in RUNAT

# Add a run time for the bot
def addRunTime(runTime):
    global RUNAT
    if not checkRunTime(runTime):
        RUNAT.append(runTime)

# Remove a run time
def removeRunTime(runTime):
    global RUNAT
    if checkRunTime(runTime):
        RUNAT.remove(runTime)

# Save the run times for the bot
def saveRunAt(storage):
    global RUNAT
    runat = j.dumps(RUNAT)
    with open(storage, "w") as saved:
        j.dump(runat, saved)
    saved.close()

# Load the run times from a file
def loadRunAt(storage):
    global RUNAT
    if findStorage(storage):
        with open(storage, "r") as saved:
            RUNAT = j.loads(j.load(saved))
        saved.close()
        return
    RUNAT = []

# Wait for a time to arrive and run the given action
def waitAndRun(action):
    """Enter action to run as lambda: functionName(*anyParameters)"""
    global RUNAT
    RUNAT.sort()
    times = []
    for rt in RUNAT:
        dt = convertToDatetime(rt)
        if datetime.today() > addSecs(dt, 10):
            dt = addDays(dt, 1)
        times.append(dt)
    
    times.sort()
    for t in times:
        while t > datetime.today():
            if not getRunning():
                return
            sleep(1)

        if datetime.today() < addSecs(t, 10):
            action()
    sleep(10)

# Test action
def act(string):
    print(string)

# Add seconds to a time
def addSecs(ct, secs):
    full = ct + timedelta(seconds=secs)
    return full

# Add days to a time
def addDays(ct, d):
    full = ct + timedelta(days=d)
    return full

# Convert a string into a datetime object
def convertToDatetime(string):
    t = string.split(":")
    now = datetime.today()
    return datetime(now.year, now.month, now.day, int(t[0]), int(t[1]), 0, 0)

if __name__ == "__main__":
    times = ["12:50", "12:51"]
    addRunTime("12:50")
    addRunTime("12:51")

    while True:
        waitAndRun(lambda: act("Hello"))
        sleep(10)
