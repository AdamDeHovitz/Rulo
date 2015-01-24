import pymongo, csv
from pymongo import Connection, MongoClient
import gridfs
from bson.objectid import ObjectId

picsDB = MongoClient().gridfs_example
fs = gridfs.GridFS(picsDB)

conn = Connection()
db = conn["rulo"]
users = db.users
events = db.events

#----------------------PIC STUFF---------------------#

def uploadPicture (picture):
    _id = fs.put(picture)
    return _id

def updatePicture (picture, user):
    _id = uploadPicture(picture)
    users.update({"uname":user},{'$set':{'pic':_id}})
    
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
    #udict['pic'] = uploadPicture(udict['pic'])
    age = udict['age']
    uncheck = users.find_one({'uname':uname}) == None
    emailcheck = users.find_one({'email':email}) == None
    agecheck = False
    validagecheck = True
    try:
        age = int(age)
        agecheck = (age > 13)
    except ValueError:
        validagecheck = False
    
    s = ""
    if uncheck == False:
        s = "That username has already been used\n"
    elif not (len(udict['pw']) >= 5 and len(udict['pw']) <= 20):
        s += "Password must be between 5 and 20 characters\n"
    elif pwcheck == False:
        s +=  "Passwords do not match"
    elif emailcheck == False:
        s += "Email has already been registered"
    elif agecheck == False:
        s += "You must be older than 13 years of age"
    elif validagecheck == False:
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

def addPerson(pdict):
    #pdict['picture'] = file; should be sent from form 
    # --> other stuff that needs to be initialized
    pdict['comments'] = []
    pdict['ratings'] = []
    pdict['uevents'] = []
    users.insert(pdict)

    
def addField(uname, field, data):
    '''
    add a new field or update an old one 
    '''
    #p = users.find_one({"fname":fname})
    #p[field] = data
    #users.save(p)
    if field == 'pic':
        updatePicture (data, uname)
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
    users.update(
        { 'uname' : uname },
        { '$push' : { 'uevents' : eventid } }
    )

def getUserEvents(uname):
    u = getUser(uname)
    es = u.get('uevents')
    return events.find( '_id' { '$in' : es } )



#--------------------------EVENT STUFF------------------------#

def createEvent(edict):
    edict['peeps'] = [edict['creator']] #list of people in event, including creator 
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
    events.update(
        {'_id' : eventid },
        { '$push' : { 'peeps' : uname } }
        )
    """
    ev = events.find_one({'_id':ObjectId( eventid ), 'peeps':{'$exists':True}})    
    if ev == None:
        return "This event doesn't exist"
    ev['peeps'].append(uname);
    """
    return ""


def getEventAttribute(eventid, field):
    ev = events.find_one( { '_id' : ObjectId( eventid ) } ) 
    if ev == None:
        return None
    return ev.get(field)



    
if __name__ == "__main__":
    
    for person in users.find():
        print person
        print "\n"
        
    
    print "-------"
    print listEvents()
    print "-------"
    

    #-----UNCOMMENT TO REMOVE ALL EVENTS/USERS-----#
    #for e in events.find():
    #    events.remove(e)
    #for p in users.find():
    #    users.remove(p)
   


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
