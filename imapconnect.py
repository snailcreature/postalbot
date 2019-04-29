# Recieve
# Code for getting data from an inbox

import imaplib as i
import email as e
import json as j

# Global information
USERNAME = ""
PASSWORD = ""
IMAP_URL = ""
CONNECT  = None

# Set the username
def setUsername(newUsername):
    global USERNAME
    USERNAME = str(newUsername)

# Set the password
def setPassword(newPassword):
    global PASSWORD
    PASSWORD = str(newPassword)

# Get the username
def getUsername():
    return USERNAME

# Get the password
def getPassword():
    return PASSWORD

# Set the IMAP url for the email server
def setImapURL(newURL):
    global IMAP_URL
    IMAP_URL = newURL

# Open a connection to the email server
def openConnection():
    global CONNECT, USERNAME, PASSWORD
    CONNECT = i.IMAP4_SSL(IMAP_URL)
    CONNECT.login(USERNAME, PASSWORD)
    CONNECT.select()

# Search the inbox for a value
def search(key, value):
    null, data = CONNECT.search(None, key, '{}'.format(value))
    del null
    return data

# Get the emails from a search
def getEmails(resultBytes):
    msgs = []
    for num in resultBytes[0].split():
        null, data = CONNECT.fetch(num, "(RFC822)")
        del null
        msgs.append(data)
    return msgs

# Get the message data from the emails
def extractMessages(emails):
    msgs = {}
    count = 0
    for mail in emails:
        msgs[count] = extractData(mail)
        count += 1
    return msgs

# Get the full inbox contents
def getInbox():
    return getEmails(search("TO", '"{}"'.format(USERNAME)))

# Get the main body data from a message
def extractData(msg):
    rawMsg = e.message_from_bytes(msg[0][1])
    reciever = rawMsg.as_string().split(" ")[1].split("\n")[0]
    body = "{}".format(getBody(rawMsg))
    return {"reciever" : reciever, "body" : body}

# Strip a message down to its main body of text
def getBody(msg):
    if msg.is_multipart():
        return getBody(msg.get_payload(0))
    return msg.get_payload(None, True)

# Save messages to a given location
def saveMessages(messages, storage):
    toSave = j.dumps(messages)
    with open(storage, "w") as saveFile:
        j.dump(toSave, saveFile)
    saveFile.close()

# Close the connection
def closeConnection():
    global CONNECT
    CONNECT.close()
    CONNECT.logout()

# Empty the inbox
def clearInbox():
    global CONNECT
    try:
        ids = search("TO", '"{}"'.format(USERNAME))
        idList = ids[0].split()
        for id in idList:
            CONNECT.store(id, '+FLAGS', r'(\Deleted)')
        CONNECT.expunge()
        return True
    except Exception as e:
        print(e)