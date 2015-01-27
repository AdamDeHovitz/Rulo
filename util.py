import pymongo, csv
from pymongo import Connection, MongoClient
import gridfs
from bson.objectid import ObjectId
import re
import os
import platform
from werkzeug import secure_filename
from datetime import datetime

#UPLOAD_LOC = R'C:\Users\Mr.Something\Documents\GitHub\Rulo\static\profilePictures'
if platform.system() == 'Windows':
  UPLOAD_LOC = R'static\profilePictures/'
else:
  UPLOAD_LOC = R'static/profilePictures/'


picsDB = MongoClient().gridfs_example
fs = gridfs.GridFS(picsDB)

conn = Connection()
db = conn["rulo"]
users = db.users
events = db.events

#----------------------PIC STUFF---------------------#

"""def uploadPicture (picture):
    print "in upload"
    print picture
    _id = fs.put(picture)
    print "uploaded"
    return _id """

def uploadPicture (picture):
  try:
    filename = secure_filename(picture.filename)
  except AttributeError:
    filename = secure_filename(picture.name)
  if not(os.path.exists(os.path.join(UPLOAD_LOC, filename))):
    print filename
    print UPLOAD_LOC
    print(type(picture))
    print (os.path.join(UPLOAD_LOC, filename))
    print "have not saved yet..."
    picture.save(os.path.join(UPLOAD_LOC, filename))
    print "saved the pic"
  return filename


"""def updatePicture (picture, user):
    print "in update"
    print type(picture)
    _id = uploadPicture(picture)
    users.update({"uname":user},{'$set':{'pic':_id}})
    print users.find_one({'uname':user})['pic']
    print "update complete"
    return _id == users.find_one({'uname':user})['pic']"""

def updatePicture (picture, user):
    print "in update"
    #print type(picture)
    filename = uploadPicture(picture)
    users.update({"uname":user},{'$set':{'pic':filename}})
    print users.find_one({'uname':user})['pic']
    print "update complete"
    return filename == users.find_one({'uname':user})['pic']


'''def getPicture (user):
    p = users.find_one({"uname":user})
    _id = p['pic']
    picture = fs.get(_id)
    return picture'''

def getPicture(user):
  print platform.system()
  print UPLOAD_LOC
  p = users.find_one({"uname":user})
  filename = p['pic']
  print type(filename)
  print filename
  path = os.path.join(UPLOAD_LOC, filename)
  path = os.path.join('..', path)
  return filename


#----------------------USER STUFF--------------------#
def newUser(udict):
    '''
    dict: fname, lname, uname, email, pw + rpw, pic
    '''
    uname = udict['uname']
    email = udict['email']
    if udict['pic'] == "default":
      udict['pic'] = "ewokPing.jpg"
    else:
      udict['pic'] = uploadPicture(udict['pic'])
    age = udict['age']
    uncheck = users.find_one({'uname':uname}) == None
    pwcheck = checkNewPW(udict['pw'], udict['rpw'])
    emailcheck = checkEmail(email)
    validagecheck = True
    agecheck = (int(age) >= 13)

    s = ""
    if uncheck == False:
      s = "That username has already been used\n"
    elif pwcheck != "":
      return pwcheck
    elif emailcheck != "":
      return emailcheck
    elif not agecheck:
      s += "You must be older than 13 years of age"
    elif not validagecheck:
      s += "Please enter a numerical age"
    else:
      print udict
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

    if e.findall(email) == []:
        return "That is not a proper email address"
    if users.find_one({'email':email}) != None:
        return "Email has already been registered"
    else:
        return ""



def addPerson(pdict):
    #pdict['picture'] = file; should be sent from form
    # --> other stuff that needs to be initialized
    pdict['reviews'] = [] # 'user', 'rating', 'comment'
    pdict['hevents'] = [] #hosted events
    pdict['revents'] = [] #requested events
    pdict['aevents'] = [] #approved events
    pdict['notifications'] = [] #event notifs
    pdict['avrate'] = 0.0
    users.insert(pdict)


def addField(uname, field, data):
    '''

    add a new field or update an old one that isn't a list

    '''
    if field == 'pic':
        print "in add"
        print type(data)
        test = updatePicture (data, uname)
        return test
    else:
        users.update( {"uname":uname} , { '$set': {field:data} } )


def updateUField(uname, field, data):
    '''
    add data to list field
    '''
    users.update(
        { 'uname' : uname },
        { '$push' : { field : data } }
    )

def updateReview(uname, review):
    updateUField(uname, 'reviews', review)
    u = getUser(uname)
    a = 0.0;
    for r in u['reviews']:
        a += r['rating']
    addField(uname, 'avrate', a/len(u['reviews']))


def addEventUserList(uname, field, eventid):
    updateUField(uname, field, ObjectId(eventid))
def removeEventUserList(uname, field, eventid):
    removeUField(uname, field, ObjectId(eventid))

def removeUField(uname, field, data):
    '''
    remove data to list field
    '''
    users.update(
        { 'uname' : uname },
        { '$pull' : { field : data } }
    )

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
'''

def getHostedEvents(uname):
    u = getUser(uname)
    es = u.get('hevents')
    return events.find( { '_id' : { '$in' : es } } )

'''
def confirmNotification(uname, eventid):


    notification = users.find_one(
        {
            uname:{
                'notifications': {
                    '$elemMatch': {
                        "id": ObjectId(eventid)
                        }
                        }
                }
            }
        )
    
  
    users.update(
        { 'uname' : uname },
        { '$pull' : { 'notifications' : notification.get('_id') }
    
    })  '''
       
    


#--------------------------EVENT STUFF------------------------#

def createEvent(edict):
    edict['requests'] = [] #Not including creator right now [edict['creator']]
    #list of people in event, including creator
    edict['members'] = []
    edict['msgs'] = [] # list of dictionaries, msgs should have: time, user, msg
    edict['open'] = True
    edict['started'] = False
    edict['datetime'] = datetime.today()
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

def updateEField(eventid, field, data):
    '''
    adds data to eventid's field array
    '''
    events.update(
        { '_id' : ObjectId(eventid) },
        { '$push' : { field : data } }
    )

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

def updateEventField(eventid, field,value):
    events.update( {"_id":ObjectId(eventid)} , { '$set': {field:value} } )

def confirmPerson(uname, eventid):
    pullEField(eventid, 'requests', uname)
    updateEField(eventid, 'members', uname)
    updateUField(uname, 'aevents', ObjectId(eventid))
    removeUField(uname, 'revents', ObjectId(eventid))
    ev = events.find_one( { '_id' : ObjectId( eventid ) } )
    print("Length: "+str(len(list(ev['members']))))
    if (ev['numb'] != "" and int(ev['numb'] ) <= (len(list(ev['members'])) + 1)):
        updateEventField(eventid, "open", False)



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

def startEvent(eventid):
    
    ev = events.find_one( { '_id' : ObjectId( eventid ) } )
    '''
    notification = {}
    notification["id"] = eventid
    notification["ename"]= ev.get("ename")
    for member in ev.get("members"):
        print(member + " getting the notification")
        users.update(
        { 'uname' : member },
        { '$push' : { 'notifications' : notification } }
        )
        '''
    events.update( {"_id":ObjectId(eventid)} , { '$set': {'started':True} } )
    print (ev.get("started"))
    for member in ev.get("members"):
        users.update(
        { 'uname' : member },
        { '$push' : { 'notifications' : eventid } }
        )
    
def validEvents(uname):
    '''
    returns a list of the events uname can join based on
    - Not already in
    - Open
    - GEOLOCATION********************!!!!!!
      - we could do some cool cs list organizing things with like a insertion sort
    '''
    evs = []
    for e in events.find():
        nc = e['creator'] != uname
        nm = uname not in e['members']
        nr = uname not in e['requests']
        if nc and nm and nr and e['open']:
            print e['open']
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
  newuser['pic'] = "default"
  newUser(newuser)

  edict = {}
  edict['creator'] = 's'
  edict['ename'] = '1st event'
  edict['numb'] = 5
  edict['desc'] = '1'
  edict['total'] = 10
  edict['price'] = 10
  edict['loc'] = 0
  edict['long'] = 0
  edict['lat'] = 0
  newevent = createEvent(edict)
  updateUField('s', 'hevents', newevent)



#--------------------------------------------------------#




if __name__ == "__main__":

    #-----COMMENT TO REMOVE ALL EVENTS/USERS-----#
    #'''
    for e in events.find():
        events.remove(e)
    for p in users.find():
        users.remove(p)
        #setup()
    #xs'''
    #------UNCOMMENT TO PRINT STUFF---------#
    #'''
    for person in users.find():
        print person
        print "\n"
    print "-------"
    print listEvents()
    #'''
    d = datetime.today()
    print type(d)



"""
Events:
'ename', u'desc', 'total', 'numb', 'price', u'long', 'lat'
'creator', u'members': [], 'requests': [],
'msgs' { 'user', 'msg' }
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
