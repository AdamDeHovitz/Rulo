from flask import flash, Flask, g, render_template, session, redirect, url_for, \
     escape, request
import util #util.py

app = Flask(__name__)
app.secret_key = 'a'


def authenticate(page):
    def yo(func):
        @wraps(func)
        def inner(*args):
            if 'username' not in session:
                session['nextpage']=page
                flash("Incorrect access, please login")
                return redirect("/login")
            result = func(*args)
            return result
        return inner
    return yo


@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    udict = {'uname':False}
    if 'username' in session:
        username = escape(session['username'])
        udict = util.getUser(username)
    return render_template('home.html', udict = udict)

@app.route('/user', methods=['POST'])
def user():
    #print("user!");
    if request.method=="POST":
        print request.form['uname']
        newuser = {}
        newuser['uname'] = request.form['uname']
        newuser['fname'] = request.form['fname']
        newuser['lname'] = request.form['lname']
        newuser['pw'] = request.form['pw']
        newuser['rpw'] = request.form['rpw']
        newuser['age'] = request.form['age'] #type = unicode
        valid_msg = util.newUser(newuser)
        if valid_msg == '':
            session['username'] = request.form['uname']
            return redirect('/home')
        else:
            flash(valid_msg)
            return redirect('/register')

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
def personal():    
    username = escape(session['username'])
    if request.method=="POST":
        submit = request.form['submit']
        if submit == 'name':
            login.addField(username,"fname",request.form["fname"])
            login.addField(username,"lname",request.form["lname"])          
        util.addField(username,submit,request.form[submit])
    return render_template('personal.html', udict=mongo.getUser(username))



if __name__ == '__main__':
    app.debug = True
    app.run()
