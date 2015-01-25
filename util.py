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
    
    uname = udict['uname']
    email = udict['email']
    udict['pic'] = uploadPicture(udict['pic'])
    age = udict['age']
    uncheck = users.find_one({'uname':uname}) == None
    pwcheck = checkNewPW(udict['pw'], udict['rpw'])
    emailcheck1 = users.find_one({'email':email}) == None
    emailcheck2 = checkEmail(email) #regex basic check
    validagecheck = True
<<<<<<< HEAD
    try:
        age = int(age)
        agecheck = (age >= 13)
    except ValueError:
        validagecheck = False
=======
    agecheck = (age >= 13)
>>>>>>> ed46dc2bd50c37842d351770b2b2e2009ec1c4e5

    s = ""
    if uncheck == False:
        s = "That username has already been used\n"
    elif pwcheck != "":
        return pwcheck
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

def checkNewPW(pw, rpw):
    if pw != rpw:
        return "Passwords do not match"
    elif not (len(pw) >= 5 and len(pw) <= 20):
        return "Password must be between 5 and 20 characters"
    else:
        return ""

def pwcheck(uname, old, new, check):
    if checkPword(uname, old) != "":
        return checkPword(uname, old)
    elif checkNewPW(new, check) != "":
        return checkNewPW(new, check)
    else:
        return ""
    
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
<<<<<<< HEAD
    print check
    return check != []
=======
    return check != [] 
>>>>>>> ed46dc2bd50c37842d351770b2b2e2009ec1c4e5

def addPerson(pdict):
    #pdict['picture'] = file; should be sent from form
    # --> other stuff that needs to be initialized
    pdict['comments'] = []
    pdict['ratings'] = []
    pdict['hevents'] = [] #hosted events
    pdict['revents'] = [] #requested events
    pdict['aevents'] = [] #approved events
    users.insert(pdict)


def addField(uname, field, data):
    '''
<<<<<<< HEAD
    add a new field or update an old one
=======
    add a new field or update an old one that isn't a list
>>>>>>> ed46dc2bd50c37842d351770b2b2e2009ec1c4e5
    '''
    if field == 'pic':
        print "in add"
        print type(picture)
        test = updatePicture (data, uname)
        return test
    else:
        users.update( {"uname":uname} , { '$set': {field:data} } )

<<<<<<< HEAD
=======
def updateUField(uname, field, data):
    '''
    add data to list field
    ''' 
    users.update(
        { 'uname' : uname },
        { '$push' : { field : data } }
    )

def addEventUserList(uname, field, eventid):
    updateUField(uname, field, ObjectId(eventid))


def removeField(uname, field, data):
    '''
    add data to list field
    '''
    users.update(
        { 'uname' : uname },
        { '$pull' : { field : data } }
    )
>>>>>>> ed46dc2bd50c37842d351770b2b2e2009ec1c4e5

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
    '''
    users.update(
        { 'uname' : uname },
        { '$push' : { 'hevents' : eventid } }
    )'''
    updateUField( uname, 'hevents', eventid)
    
    
def getRequestedEvents(uname):
    u = getUser(uname)
    es = u.get('revents')
    print "revents"
    print es
    return events.find( { '_id' : { '$in' : es } } )

def getApprovedEvents(uname):
    u = getUser(uname)
    es = u.get('aevents')
    return events.find( { '_id' : { '$in' : es } } )
'''
eventList = list(getUserEvents(uname))
    approved = []
    print(eventList)
    for event in eventList:
        print (event)
        if uname in event["members"]:
            approved.append(event)
    return approved
<<<<<<< HEAD


=======
'''        
    
>>>>>>> ed46dc2bd50c37842d351770b2b2e2009ec1c4e5
def getHostedEvents(uname):
    u = getUser(uname)
    es = u.get('hevents')
    return events.find( { '_id' : { '$in' : es } } )



#--------------------------EVENT STUFF------------------------#

def createEvent(edict):
<<<<<<< HEAD
    edict['requests'] = [] #Not including creator right now [edict['creator']] #list of people in event, including creator
    edict['members'] = []
    return events.insert(edict)


def listEvents():
    eventslist = []
    for e in events.find():
        eventslist.append(e)
    return eventslist
=======
    edict['requests'] = [] #Not including creator right now [edict['creator']]
    #list of people in event, including creator 
    edict['members'] = []
    edict['msgs'] = [] # list of dictionaries, msgs should have: time, user, msg
    e = events.insert(edict)
    #print e
    return e #returns w/o objectid( )


def checkEvent(edict):
     # check for required inputs (name, description)
    if edict['ename'] == "":
        return "Input a name for your event"
    if edict['desc'] == '    ' or edict['desc'] == '':
        return "Input a description for your event"
    else:
        return ""
>>>>>>> ed46dc2bd50c37842d351770b2b2e2009ec1c4e5

def updateEField(eventid, field, data):
    '''
    adds data to eventid's field array 
    '''
    events.update(
        { '_id' : ObjectId(eventid) },
<<<<<<< HEAD
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
=======
        { '$push' : { field : data }}
    )
>>>>>>> ed46dc2bd50c37842d351770b2b2e2009ec1c4e5

def pullEField(eventid, field, data):
    events.update(
        { '_id' : ObjectId(eventid) },
        { '$pull' : { field : data } }
    )

def getEventAttribute(eventid, field):
    ev = events.find_one( { '_id' : ObjectId( eventid ) } )
    if ev == None:
        return None
    return ev.get(field)


def listEvents():
    eventslist = []
    for e in events.find():
        eventslist.append(e)
    return eventslist

    

def confirmPerson(uname, eventid):
    pullEField(eventid, 'requests', uname)
    updateEField(eventid, 'members', uname)



def getEvent(eventid):
    print("id:")
    print(eventid)
    return events.find_one( { '_id' :  ObjectId(eventid)  } )

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
<<<<<<< HEAD

=======
    
def eventsNotIn(uname):
    '''
    returns a list of the events uname is not already involved with
    '''
    evs = []
    for e in events.find():
        nc = e['creator'] != uname
        nm = uname not in e['members']
        nr = uname not in e['requests']
        if nc and nm and nr:
            evs.append(e)
    return evs

#----------------------------------------#
def setup():
    newuser = {}
    newuser['uname'] = 's'
    newuser['fname'] = 's'
    newuser['lname'] = 's'
    newuser['pw'] = 'sssss'
    newuser['rpw'] = 'sssss'
    newuser['age'] = 18 
    newuser['email'] = 's@g.c'
    newUser(newuser)

    edict = {}
    edict['creator'] = 's'
    edict['ename'] = '1st event'
    edict['numb'] = 5
    edict['desc'] = '1'
    edict['total'] = 10
    edict['price'] = 10 
    edict['long'] = 0   
    edict['lat'] = 0
    newevent = createEvent(edict)
    updateUField('s', 'hevents', newevent)



#--------------------------------------------------------#
>>>>>>> ed46dc2bd50c37842d351770b2b2e2009ec1c4e5




if __name__ == "__main__":
       
    #print eventsNotIn('s')
    
    #-----COMMENT TO REMOVE ALL EVENTS/USERS-----#
    '''
    for e in events.find():
        events.remove(e)
    for p in users.find():
        users.remove(p)
    setup()
    '''
    #------UNCOMMENT TO PRINT STUFF---------#
    #'''
    for person in users.find():
        print person
        print "\n"
<<<<<<< HEAD


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

=======
    print "-------"
    print listEvents()
    #'''
    
>>>>>>> ed46dc2bd50c37842d351770b2b2e2009ec1c4e5
"""
Events:
'ename', u'desc', 'total', 'numb', 'price', u'long', 'lat'
'creator', u'members': [], 'requests': [],
u'_id': ObjectId('54c51e6067a8a20244124da7')

Users:
'uname', 'hevents', 'revents', 'aevents'

    
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
