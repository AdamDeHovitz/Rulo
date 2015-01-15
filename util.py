import pymongo, csv
from pymongo import Connection


conn = Connection()
db = conn["rulo"]
users = db.users
events = db.events

#----------------------USER STUFF--------------------#
def newUser(udict):
    '''
    dict: fname, lname, uname, email, pw + rpw, pic 
    '''
    pwcheck = (udict['pw'] == udict['rpw'])
    uname = udict['uname']
    email = udict['email']
    pic = udict['pic']
    uncheck = users.find_one({'uname':uname}) == None
    emailcheck = users.find_one({'email':email}) == None
    s = ""
    if uncheck == False:
        s = "That username has already been used\n"
    elif not (len(udict['pw']) >= 5 and len(udict['pw']) <= 20):
        s += "Password must be between 5 and 20 characters\n"
    elif pwcheck == False:
        s +=  "Passwords do not match"
    elif emailcheck == False:
        s += "Email has already been registered"
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
    #pdict['events'] = []
    #pdict['picture'] = file; should be sent from form 
    # --> other stuff that needs to be initialized
    pdict['comments'] = []
    pdict['ratings'] = []
    
    users.insert(pdict)

def addField(uname, field, data):
    '''
    add a new field or update an old one 
    '''
    #p = users.find_one({"fname":fname})
    #p[field] = data
    #users.save(p)
    users.update({"uname":uname},{'$set':{field:data}})

def getUser(uname):
    return users.find_one({'uname':uname})

def getAttribute(uname, field):
    ret = users.find_one({'uname':uname, field:{'$exists':True}})
    if ret == None:
        return None
    ret = ret.get(field)
    #print(ret)
    return ret



#--------------------------EVENT STUFF------------------------#

def createEvent(edict):
    events.insert(edict)

def listEvents():
    eventslist = []
    for e in events.find():
        eventslist.append(e)
    return eventslist


if __name__ == "__main__":
    #for person in users.find():
    #    users.remove(person)
    print listEvents()

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
