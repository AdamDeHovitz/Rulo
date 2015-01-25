import pymongo, csv
from pymongo import Connection, MongoClient
import gridfs
from bson.objectid import ObjectId
import re

picsDB = MongoClient().gridfs_example
fs = gridfs.GridFS(picsDB)

conn = Connection()
db = conn["rulo"]
users = db.users
events = db.events

#----------------------PIC STUFF---------------------#

def uploadPicture (picture):
    print "in upload"
    print picture
    _id = fs.put(picture)
    return _id

def updatePicture (picture, user):
    print "in update"
    print type(picture)
    _id = uploadPicture(picture)
    users.update({"uname":user},{'$set':{'pic':_id}})
    print users.find_one({'uname':user})['pic']
    return _id == users.find_one({'uname':user})['pic']

def getPicture (user):
    p = users.find_one({"uname":user})
    _id = p['pic']
    picture = fs.get(_id)
    return picture

#----------------------USER STUFF--------------------#
def newUser(udict):
    '''
    dict: fname, lname, uname, email, pw + rpw, pic
    '''
    pwcheck = (udict['pw'] == udict['rpw'])
    uname = udict['uname']
    email = udict['email']
    udict['pic'] = uploadPicture(udict['pic'])
    age = udict['age']
    uncheck = users.find_one({'uname':uname}) == None
    emailcheck1 = users.find_one({'email':email}) == None
    emailcheck2 = checkEmail(email) #regex basic check
    agecheck = False
    validagecheck = True
    try:
        age = int(age)
        agecheck = (age >= 13)
    except ValueError:
        validagecheck = False

    s = ""
    if uncheck == False:
        s = "That username has already been used\n"
    elif not (len(udict['pw']) >= 5 and len(udict['pw']) <= 20):
        s += "Password must be between 5 and 20 characters"
    elif not pwcheck:
        s +=  "Passwords do not match"
    elif not emailcheck1:
        s += "Email has already been registered"
    elif not emailcheck2:
        s += "That is not a proper email address"
    elif not agecheck:
        s += "You must be older than 13 years of age"
    elif not validagecheck:
        s += "Please enter a numerical age"
    else:
        addPerson(udict)
    return s

def checkPword(uname,pw):
    rpw = getAttribute(uname,"pw")
    if rpw == None:
        return "Username does not exist"
    if rpw == pw:
        return ""
    else:
        return "Wrong password"

def checkEmail(email):
    e = re.compile("[^@]+@[A-z]+\..+")
    check = e.findall(email)
    print check
    return check != []

def addPerson(pdict):
    #pdict['picture'] = file; should be sent from form
    # --> other stuff that needs to be initialized
    pdict['comments'] = []
    pdict['ratings'] = []
    pdict['uevents'] = []
    pdict['hevents'] = []
    users.insert(pdict)


def addField(uname, field, data):
    '''
    add a new field or update an old one
    '''
    #p = users.find_one({"fname":fname})
    #p[field] = data
    #users.save(p)
    if field == 'pic':
        print "in add"
        print type(picture)
        test = updatePicture (data, uname)
        return test
    else:
        users.update( {"uname":uname} , { '$set': {field:data} } )


def getUser(uname):
    return users.find_one({'uname':uname})


def getAttribute(uname, field):
    #return getUser(uname).get(field) [field]
    u = users.find_one(
        { 'uname' : uname ,
          field: { '$exists' : True } } )
    if u == None:
        return None
    return u.get(field)


def addEventPerson(eventid, uname):
    '''
    adding an event id to a person
    '''
    eventid = ObjectId(eventid)
    users.update(
        { 'uname' : uname },
        { '$push' : { 'uevents' : eventid } }
    )

def addHostPerson(eventid, uname):
    users.update(
        { 'uname' : uname },
        { '$push' : { 'hevents' : eventid } }
    )
def getUserEvents(uname):
    u = getUser(uname)
    es = u.get('uevents')
    return events.find( { '_id' : { '$in' : es } } )

def getApprovedEvents(uname):
    eventList = list(getUserEvents(uname))
    approved = []
    print(eventList)
    for event in eventList:
        print (event)
        if uname in event["members"]:
            approved.append(event)

    return approved


def getHostedEvents(uname):
    u = getUser(uname)
    es = u.get('hevents')
    return events.find( { '_id' : { '$in' : es } } )



#--------------------------EVENT STUFF------------------------#

def createEvent(edict):
    edict['requests'] = [] #Not including creator right now [edict['creator']] #list of people in event, including creator
    edict['members'] = []
    return events.insert(edict)


def listEvents():
    eventslist = []
    for e in events.find():
        eventslist.append(e)
    return eventslist

def addPersonEvent(uname, eventid):
    '''
    adding a person to an event
    '''
    #'''
    events.update(
        { '_id' : ObjectId(eventid) },
        { '$push' : { 'requests' : uname } }
        )
    #print(getEventAttribute(eventid, 'requests'))
    """
    ev = events.find_one({'_id':ObjectId( eventid ), 'requests':{'$exists':True}})
    if ev == None:
        return "This event doesn't exist"
    ev['requests'].append(uname);
    for u in ev['requests']:
        print(u)
        """
    return ""

def confirmPerson(uname, eventid):

    events.update(
        { '_id' : ObjectId(eventid) },
        { '$pull' : { 'requests' : uname } }
        )
    events.update(
        { '_id' : ObjectId(eventid) },
        { '$push' : { 'members' : uname } }
        )

def getEventAttribute(eventid, field):
    ev = events.find_one( { '_id' : ObjectId( eventid ) } )
    if ev == None:
        return None
    return ev.get(field)

def getEvent(eventid):
    print("id:")
    print(eventid)
    return events.find( { '_id' :  ObjectId(eventid)  } )

def deleteEvent(eventid):
    ev = events.find_one( { '_id' : ObjectId( eventid ) } )

    #Removing all of the types of people in the event
    people = []
    for user in ev.get("requests"):
        people.append(user)
    for member in ev.get("members"):
        people.append(member)
    for user in people:
        users.update(
        { 'uname' : user },
        { '$pull' : { 'uevents' : eventid } }
    )
        #Don't forget the host
    users.update(
        { 'uname' : ev.get("creator") },
        { '$pull' : { 'hevents' : eventid } }
    )

    #Now let's remove the event itself
    events.remove(ev)





if __name__ == "__main__":
    '''
    for person in users.find():
        print person
        print "\n"


    print "-------"
    print listEvents()
    print "-------"
    '''

    #-----COMMENT TO REMOVE ALL EVENTS/USERS-----#
    #'''
    for e in events.find():
        events.remove(e)
    for p in users.find():
        users.remove(p)
        #'''

"""
 people = db.people

 to insert
     people.insert(dict)
 to update:
     person = people.find_one({"food":"ham"})
     person["food"] = "eggs"
     people.save(person)
 to remove:
     for person in people.find():
        people.remove(person)
 people.find(dict) --> returns a list of people with the dict qualities
 users.remove({"fname":{"$exists":False}})
"""
