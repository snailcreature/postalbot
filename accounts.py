# Account tracking for Postalbot

import json as j
import pathlib as p

# A dictionary of usernames and emails
ACCOUNTS = {}

# Return the accounts
def getAccounts():
    return ACCOUNTS

# Add an account; key = username, value = email
def addAccount(key, value):
    if not findAccount(key):
        ACCOUNTS[key] = value
        return True
    return False

# Remove an account; key = username
def removeAccount(key):
    if findAccount(key):
        del ACCOUNTS[key]
        return True
    return False

# Update the email of an account
def updateAccountEmail(key, newValue):
    if findAccount(key):
        ACCOUNTS[key] = newValue
        return True
    return False

# Update the username of an account
def updateAccountName(key, newKey):
    if findAccount(key):
        hold = ACCOUNTS[key]
        removeAccount(key)
        addAccount(newKey, hold)
        del hold
        return True
    return False

# Check if an account exists
def findAccount(key):
    if key in ACCOUNTS.keys():
        return True
    return False

# Return an account, if it exists
def getAccount(key):
    if findAccount(key):
        return ACCOUNTS[key]
    return None

# Check a storage location exists
def findStorage(storage):
    if p.Path(storage).exists():
        return True
    return False

# Save accounts data
def saveAccounts(storage):
    global ACCOUNTS
    accounts = j.dumps(ACCOUNTS)
    with open(storage, "w") as saved:
        j.dump(accounts, saved)
    saved.close()

# Load the accounts from storage
def loadAccounts(storage):
    global ACCOUNTS
    if findStorage(storage):
        with open(storage, "r") as saved:
            ACCOUNTS = j.loads(j.load(saved))
        saved.close()
        return
    clearAccounts()

# Delete all accounts
def clearAccounts():
    global ACCOUNTS
    ACCOUNTS = {}

if __name__ == "__main__":
    loadAccounts("accounts.json")

    print(getAccount("hello"))

    addAccount("jerry", "jerry@example.net")

    saveAccounts("accounts.json")

    print(getAccount("jerry"))

    clearAccounts()
    saveAccounts("accounts.json")

    print(getAccount("jerry"))