import pymongo, csv
from pymongo import Connection

conn = Connection()
db = conn["rulo"]
people = db.people
events = db.events

def newUser(dict):
    people.insert(dict)

# dict should have name, username, etc 

def newEvent(ev):
    events.insert(ev)
