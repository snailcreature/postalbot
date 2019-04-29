# Sorting
# Sort the mail

import json as j
from datetime import datetime as d

import accounts as a

# Extract the the username from an incoming email
def extractUsername(email):
    return email.split("+")[1].split("@")[0]

# Load the messages stored at a location
def loadMessages(storage):
    if a.findStorage(storage):
        with open(storage, "r") as f:
            msgs = j.loads(j.load(f))
        f.close()
        return msgs
    return None

# Sort the messages into the outbox and the archive
def sortMessages(messages):
    for key in messages.keys():
        reciever, body = messages[key].values()
        body = fixFormatting(body[2:-1])
        try:
            reciever = extractUsername(reciever)
            if reciever in a.ACCOUNTS.keys():
                saveMessage(reciever, body)
                appendToMail(reciever, body)
        except:
            continue

# Save a message to the archive
def saveMessage(name, body):
    n = d.now()
    fileName = "{}-{}-{}-{}{}--{}-{}.txt".format(n.year, n.month, n.day, n.hour, name, n.minute, n.microsecond)
    fileName = "resources/saved/"+fileName
    with open(fileName, "w") as saved:
        saved.write(body)
    saved.close()

# Add a message to the outbox of a user
def appendToMail(name, body):
    fileName = "resources/outbox/{}.json".format(name)

    if a.findStorage(fileName):
        with open(fileName, "r") as openFile:
            currentMail = j.loads(j.load(openFile))
        openFile.close()

        currentMail[len(currentMail.keys())] = body
    
    else:
        currentMail = {0 : body}

    toSave = j.dumps(currentMail)
    with open(fileName, "w") as openFile:
        j.dump(toSave, openFile)
    openFile.close()

# Fix formatting errors caused by email conversions
def fixFormatting(text):
    fixes = {"n":"\n", "r":"\r", "t":"\t", "xe2\\x80\\x99":"\'", "xe2\\x80\\x98":"\'",
             "xe2\\x80\\x9c": "\"", "xe2\\x80\\x9d":"\"", "xe2\\x80\\xa6":"..."}

    for fix in fixes.keys():
        splitUp = text.split("\\{}".format(fix))
        text = fixes[fix].join(splitUp)
    
    return ''.join(splitUp)