# Postalbot
# A bot that emulates the postal service via email

from accounts import *
from imapconnect import *
from sorting import *
from sending import *
from waiting import *

import threading as t
from getpass import getpass

# Goes through the full process of fetching, sorting, and redistributing the letters
def delivery():
    openConnection()
    print("Connected")
    msgs = getInbox()
    data = extractMessages(msgs)
    print("Messages recieved and extracted")
    saveMessages(data, "resources/inbox/inbox.json")
    print("Messages saved")
    clearInbox()
    print("Inbox empty")
    closeConnection()
    print("Connection closed")
    sortMessages(loadMessages("resources/inbox/inbox.json"))
    print("Messages sorted")
    distribute()
    print("Messages sent")
    clearOutbox()
    print("Outbox cleared")

# Runs the main wait loop
def mainLoop():
    print("Main loop started")

    loadAccounts("resources/data/accounts.json")
    loadRunAt("resources/data/runat.json")

    while getRunning():
        waitAndRun(lambda: delivery())
    
    print("Closed")

# Allows for command line control of PostalBot
def terminal():
    choice = "help"
    while choice != "exit":
        # Command extraction and running
        split = choice.split(" ")
        mainChoice = split[0]
        if mainChoice == "help":
            print("""
COMMANDS
[~]
status - reports if the bot is running
runtimes - gets a list of the times the mail is set to come
exit - stops the bot if running and closes the program

[-]
start - starts the bot
add - adds a value to a specified object
    add runtime - takes a single value; 24hr time formatted hh:mm
    add account - takes two values; a username, an email
remove - removed a value from a specified object
    remove runtime - takes a single value; 24hr time formatted hh:mm
    remove account - takes two values; a username, an email

[+]
stop - stops the bot
manual - allows you to manually trigger events
    manual pull - downloads and sorts the emails in the inbox
    manual push - distributes sorted messages""")

        elif mainChoice == "status":
            print("Running: {}".format(getRunning()))
            print("Connection: {}".format(testConnection()))
        
        elif mainChoice == "runtimes":
            rts = getRunAt()
            rts.sort()
            if len(rts) > 1:
                for x in range(len(rts)-1):
                    print(rts[x], end=", ")
            print("{}".format(rts[-1]))

        elif mainChoice == "exit":
            print("Stopping...")
            if getRunning():
                toggleRunning()

        else:
            if not getRunning():
                if mainChoice == "start":
                    toggleRunning()
                    main = t.Thread(target=mainLoop)
                    main.start()
                
                elif mainChoice == "add":
                    if split[1] == "runtime":
                        addRunTime(split[2])
                        saveRunAt("resources/data/runat.json")
                        print("Run Time added")
                    elif split[1] == "account":
                        addAccount(split[2], split[3])
                        print("Account made")
                        saveAccounts("resources/data/accounts.json")
                        print("Account saved")
                    else:
                        print("Invalid Entry")
                
                elif mainChoice == "remove":
                    if split[1] == "runtime":
                        removeRunTime(split[2])
                        saveRunAt("resources/data/runat.json")
                        print("Account removed")
                    elif split[1] == "account":
                        removeAccount(split[2])
                        saveAccounts("resources/data/accounts.json")
                    else:
                        print("Invalid Entry")
                else:
                    print("Invalid Entry")
            else:
                if mainChoice == "manual":
                    if split[1] == "pull":
                        openConnection()
                        print("Connected")
                        msgs = getInbox()
                        data = extractMessages(msgs)
                        print("Messages recieved and extracted")
                        saveMessages(data, "resources/inbox/inbox.json")
                        print("Messages saved")
                        clearInbox()
                        print("Inbox empty")
                        closeConnection()
                        print("Connection closed")
                        sortMessages(loadMessages("resources/inbox/inbox.json"))

                    elif split[1] == "push":
                        distribute()
                        print("Messages sent")
                        clearOutbox()
                        print("Outbox cleared")

                    else:
                        print("Invalid entry")

                elif mainChoice == "stop":
                    toggleRunning()
                    main.join()
                else:
                    print("Invalid entry")
        # Formatting
        if getRunning():
            insert = "+"
        else:
            insert = "-"
        choice = input("\n[{}] >> ".format(insert)).lower()
            
    try:
        main.join()
    except:
        pass
    print("Finished")

# Test the connection to the mailbox
def testConnection():
    try:
        openConnection()
        closeConnection()
        return True
    except:
        return False

# Run if the file is run, not imported
if __name__ == "__main__":

    setUsername("username@example.com")
    setPassword("password")
    print("Username + Password")

    setImapURL("imap.gmail.com")

    setSmtpUrl("smtp.gmail.com")
    setSmtpPrt(587)
    print("Connection settings")

    loadAccounts("resources/data/accounts.json")
    addAccount("sam", "sam.drage@mac.com")
    addAccount("tom", "thomasapter@btinternet.com")
    print("Accounts made")
    saveAccounts("resources/data/accounts.json")
    print("Accounts saved")

    loadRunAt("resources/data/runat.json")
    addRunTime("15:00")
    saveRunAt("resources/data/runat.json")

    term = t.Thread(target=terminal)
    term.start()

