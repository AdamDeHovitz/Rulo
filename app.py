from flask import flash, Flask, g, render_template, session, redirect, url_for, \
     escape, request, send_from_directory
import util #util.py
from functools import wraps
import os
import platform
#import Image
from werkzeug import secure_filename
from datetime import datetime



#---------pic stuff------#
ALLOWED_FILES = set(['jpg', 'gif', 'png', 'jpeg', 'tif', 'tiff', 'jif', 'jfif', 'fpx'])

#UPLOAD_LOC = R'C:\Users\Mr.Something\Documents\GitHub\Rulo\static\profilePictures'
if platform.system == 'Windows':
  UPLOAD_LOC = R'static\profilePictures/'
else:
  UPLOAD_LOC = R'static/profilePictures/'

app = Flask(__name__, static_folder='static')
app.secret_key = 'a'
app.config['UPLOAD_LOC'] = UPLOAD_LOC



def authenticate(func):
    @wraps(func)
    def inner(*args):
        if 'username' not in session:
            session['nextpage']='/'
            flash("Incorrect access, please login")
            return redirect("/login")
        username = escape(session['username'])
        result = func(*args)
        return result
    return inner


def isFileAllowed (filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_FILES


@app.route('/')
def index():
    return redirect('/home')


@app.route('/gps')
def gps():
    return render_template("GPS.html");


@app.route('/home')
def home():
    udict = {'uname':False}
    if 'username' in session:
        username = escape(session['username'])
        udict = util.getUser(username)
        return redirect('/events')
    return render_template('home.html', udict = udict)



@app.route('/user', methods=['POST', 'GET'])
def user():
    #print("user!");
    if request.method=="POST":
        newuser = {}
        newuser['uname'] = request.form['uname']
        newuser['fname'] = request.form['fname']
        newuser['lname'] = request.form['lname']
        newuser['pw'] = request.form['pw']
        newuser['rpw'] = request.form['rpw']
        newuser['age'] = request.form['age']
        newuser['email'] = request.form['email']
        #print type(send_from_directory("/static/profilePictures", 'ewokPing.jpg'))
        #img = send_from_directory("/static/profilePictures", 'ewokPing.jpg')
        #img = file('static/profilePictures/ewokPing.jpg')
        #stepOne = Image.open('static/ewokPing.jpg')
        #img = stepOne.load()
        #print img.read()
        img = "default"
        print '\n\nDefault image assigned to newuser'
        newuser['pic'] = img

        valid_msg = util.newUser(newuser)
        print("Good?")
        if valid_msg == '':
            session['username'] = request.form['uname']
            return redirect('/home')
        else:
            flash(valid_msg)
            return redirect('/register')

@app.route('/proPic', methods=['GET', 'POST'])
@authenticate
def changePic():
  username = session['username']
  if request.method == "POST":
    img = request.files['pic']
    if img and isFileAllowed(img.filename):
      success = util.addField(session['username'], 'pic', img)
      if success:
        return redirect('/personal')
      else:
        return redirect('/personal')


@app.route('/login')
def login():
    return render_template('login.html', udict={'uname':False})


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html', udict={'uname':False})


@app.route('/register')
def register():
    return render_template('register.html', udict={'uname':False})


@app.route('/verify', methods=['POST'])
def verify():
    if request.method=="POST":
        uname = request.form['uname']
        pw = request.form['pw']
        valid_msg = util.checkPword(uname,pw)
        if valid_msg == '':
            session['username'] = uname
            return redirect('/home')
        else:
            flash(valid_msg)
            return redirect('/login')


@app.route('/personal', methods=['GET','POST'])
@authenticate
def p():
    username = escape(session['username'])
    picture = util.getPicture (session['username'])
    return render_template('personal.html', udict=util.getUser(username), change = "Null", profile = picture)


@app.route('/personal_process', methods=['POST'])
@authenticate
def personal_process():
    username = escape(session['username'])
    if request.method=="POST":
        submit = request.form['submit']
        if submit == 'name':
            util.addField(username,"fname",request.form["fname"])
            util.addField(username,"lname",request.form["lname"])
        elif submit == 'email':
            if util.checkEmail(request.form['email']) == "":
                util.addField(username, submit, request.form[submit])
            else:
                flash(util.checkEmail(request.form['email']))
        elif submit == 'pw':
            old = request.form['oldpw']
            new = request.form['pw']
            ch = request.form['cpw']
            msg = util.pwcheck(username,old,new,ch)
            if msg != "":
                flash(msg)
            else:
                util.addField(username, submit, new)
                flash("Successfully updated password")
        else:
            util.addField(username, submit, request.form[submit])
    return redirect('/personal')

@authenticate
@app.route('/personal/<thing>', methods=['GET', 'POST'])
def personal(thing = None):
    username = escape(session['username'])
    udict = util.getUser(username)
    pic = util.getPicture (udict['uname'])
    print pic
    return render_template('personal.html', udict=udict, change=thing, profile = pic)


@app.route('/create_events', methods=['GET','POST'])
@authenticate
def event_create():
    username = escape(session['username'])

    return render_template('eventCreate.html', udict=util.getUser(username))


@app.route('/create_event_process', methods=['POST'])
def process():
    if request.method=="POST":
        username = escape(session['username'])
        edict = {}
        edict['creator'] = username
        edict['ename'] = request.form["ename"]
        edict['numb'] = request.form["numb"]
        edict['desc'] = request.form["desc"]
        edict['total'] = request.form["total"]
        edict['price'] = request.form["price"]
        edict['long'] = request.form["long"]
        edict['lat'] = request.form["lat"]
        print('looking for location')
        edict['location'] = request.form['loc']
        print('got location')
        print('looking for address')
        edict['address'] = request.form['address']
        print('got address')
        if util.checkEvent(edict) != "":
            flash(util.checkEvent(edict))
            return redirect('/create_events')
        newevent = util.createEvent(edict)
        print newevent
        #util.addEventPerson(username, newevent)
        #util.addHostPerson(newevent, username)
        util.updateUField(username, 'hevents', newevent)
        return redirect('/events')
    #return render_template('eventCreated.html', udict=util.getUser(username), edict=edict)


@app.route('/events', methods=['GET','POST'])
@authenticate
def events():
    username = escape(session['username'])
    udict = util.getUser(username)
    #elist = util.listEvents();
    elist = util.validEvents(username)
    return render_template('events.html', udict=udict, elist=elist)


@app.route('/joinevent', methods=['GET','POST']) #does order matter?
@authenticate
def joinevent():
    username = escape(session['username'])
    udict = util.getUser(username)
    #elist = util.listEvents(); # do we need this?
    elist = util.validEvents(username)
    if request.method=="POST":
        event = request.form["submit"] # objectid
        #print event
        util.updateEField(event, 'requests', username)
        #util.updateUField(username, 'requests', event) #event doesn't include objectid
        util.addEventUserList(username, 'revents', event)
        #util.addEventPerson(event, username)
        return render_template('events.html', udict=udict, elist=elist,
                               name = util.getEventAttribute(event, "ename"))

@authenticate
@app.route('/your_events', methods=['GET','POST'])

def your_event():
    username = escape(session['username'])
    udict = util.getUser(username)
    all_lists =[]
    all_lists.append(util.getHostedEvents(username))
    all_lists.append(util.getApprovedEvents(username))
    all_lists.append(util.getRequestedEvents(username))

    return render_template('your_events.html', udict = udict, alist = all_lists)

@authenticate
@app.route('/confirm/<event>/<uname>', methods=['GET', 'POST'])
def confirm(event = None, uname = None):
    util.confirmPerson(uname, event)

    return redirect('/your_events')

@authenticate
@app.route('/delete_event/<id>', methods=['GET', 'POST'])
def delete(id = None):
    util.deleteEvent(id)

    return redirect(request.form["submit"])

@authenticate
@app.route('/user/<uname>', methods=['GET', 'POST'])
def user_page(uname = None):

    #if util. ---this will check if the uname exists
    if util.getUser(uname) == None:
        flash("That's not a user")
        return redirect('/events')
    else:
        username = escape(session['username'])
        udict = util.getUser(username)
        pdict = util.getUser(uname)
        pic = util.getPicture (udict['uname'])

    if request.method=="POST":
            print(request.form["rating"])


    return render_template('user.html', udict = udict, pdict=pdict, profile = pic)

@app.route('/addreview/<uname>', methods=['GET', 'POST'])
def addreview(uname = None):
    username = escape(session['username'])
    udict = util.getUser(username)
    review = {}
    review['user'] = username
    review['rating'] = int(request.form["rating"])
    review['comment'] = request.form["comment"]
    #util.updateUField(uname, 'reviews', review)
    util.updateReview(uname, review)
    return redirect('/user/'+ uname)

@authenticate
@app.route('/event_page/<id>', methods=['GET', 'POST'])
def event_page(id = None):
    if request.method=="POST":
        value = request.form["submit"]
        if (value == "close"):
            util.updateEventField(id, "open", False)
        elif (value == "start"):
            util.startEvent(id);
    username = escape(session['username'])
    udict = util.getUser(username)
    event = util.getEvent(id)
    return render_template('event_page.html', udict = udict, event = event)



@authenticate
@app.route('/event_page/<eventid>/<uname>', methods=['GET', 'POST'])
def confirme(eventid = None, uname = None):
    util.confirmPerson(uname, eventid)
    return redirect('/event_page/'+ eventid )

@authenticate
@app.route('/confirm_notification/<eventid>', methods=['GET', 'POST'])
def confirm_event(eventid = None):
    username = escape(session['username'])
    #util.confirmNotification(username, eventid)
    util.removeUField(username, 'notifications', eventid)
    return redirect('/event_page/'+ eventid )


@authenticate
@app.route('/newmsg/<eventid>', methods=['GET', 'POST'])
def newmsg(eventid = None):
    username = escape(session['username'])
    udict = util.getUser(username)
    msg = {}
    msg['user'] = username
    msg['msg'] = request.form["msg"]
    msg['time'] = datetime.today()
    util.updateEField(eventid, 'msgs', msg)

    return redirect('/event_page/'+ eventid )

@app.route('/about')
def about():
    udict = {'uname':False}
    return render_template('about.html', udict=udict) 
  

if __name__ == '__main__':
    app.debug = True
    app.run()
