# Sending
# Redistribute the mail

import smtplib as s
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import json as j
import os as o

import accounts as a
import imapconnect as i

# Global connection information
SMTP_URL = "smtp.gmail.com"
SMTP_PRT = 587

# Set the SMTP url
def setSmtpUrl(newUrl):
    global SMTP_URL
    SMTP_URL = newUrl

# Set the SMTP port of the email server
def setSmtpPrt(newPort):
    global SMTP_PRT
    SMTP_PRT = newPort

# Create an email from a username and a body of text
def makeEmail(name, body):
    address = a.getAccount(name)

    eml = MIMEMultipart()
    eml["From"] = i.USERNAME
    eml["To"] = address
    eml["Subject"] = "The Postwoman's been..."

    eml.attach(MIMEText(body, 'plain'))

    textEml = eml.as_string()

    return textEml

# Send an email containing body to user with username name
def sendEmail(name, body):

    email = makeEmail(name, body)
    address = a.getAccount(name)

    server = s.SMTP(SMTP_URL, SMTP_PRT)
    
    server.starttls()
    server.login(i.getUsername(), i.getPassword())
    
    server.sendmail(i.getUsername(), address, email)
    server.quit()

# Distribute mail to users
def distribute():
    for key in a.ACCOUNTS.keys():
        location = "resources/outbox/{}.json".format(key)
        if a.findStorage(location):
            with open(location, "r") as store:
                msgs = j.loads(j.load(store))
            store.close()

            for msg in msgs.values():
                sendEmail(key, msg)

# Empty the outbox folder
def clearOutbox():
    path = "{}/resources/outbox".format(o.path.dirname(__file__))
    if a.findStorage(path):
        fileList = o.listdir(path)
        for f in fileList:
            o.remove(o.path.join(path, f))
