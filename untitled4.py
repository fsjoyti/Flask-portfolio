from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request , redirect
from flask import  url_for
from flask import session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Nick123@localhost/test1'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password= db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(80), unique=False)
    bio = db.Column(db.TEXT(22000), unique=False)
    project1 = db.Column(db.TEXT(52000), unique=False)
    project2 = db.Column(db.TEXT(52000), unique=False)
    project3 = db.Column(db.TEXT(32000), unique=False)
    def __init__(self, email, password,username,bio,project1,project2,project3):
        self.email = email
        self.password = password
        self.username = username
        self.bio = bio
        self.project1 = project1
        self.project2 = project2
        self.project3 = project3

    def __repr__(self):
        return '<User %r>' % self.email

@app.route('/')
def index():
    return render_template('add_user.html')

@app.route('/signup', methods =['POST'])
def post():
    user = User(request.form['username'].encode('UTF-8'),request.form['email'].encode('UTF-8'),request.form['password'].encode('UTF-8'), request.form['bio'].encode('UTF-8'),request.form['project1'].encode('UTF-8'),request.form['project2'].encode('UTF-8'),request.form['project3'].encode('UTF-8'))
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['email'],
                       request.form['password']):
            return redirect(url_for('log_the_user_in'))
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('Login.html', error=error)


def valid_login(email,password):
    user = User.query.filter(User.email== email, User.password == password).first()

    if user is None:

        return False
    else:

        session["email"] = user.email
        if user.username is not None:
            session['username'] = user.username
        else:
            session['username'] = " "

        if user.bio is not None:
            session['bio'] = user.bio
        else:
            session['bio'] = " "
        if user.project1 is not None:
            session['project1'] = user.project1
        else:
            session['project1'] = " "
        if user.project2 is not None:
            session['project2'] = user.project2
        else:
            session['project2'] = " "
        if user.project3 is not None:
            session['project3'] = user.project3
        else:
            session['project3'] = " "


        return True


@app.route('/profile', methods=['GET'])
def log_the_user_in():
    email = session['email']
    username = session['username']
    bio = session['bio']
    project1 = session['project1']
    project2 = session['project2']
    project3 = session['project3']
    return render_template('profile.html', username=username, email=email, bio=bio, project1=project1, project2=project2, project3=project3)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/update', methods=['GET','POST'])
def update():
    email = session['email']
    username = session['username']
    bio = session['bio']
    project1 = session['project1']
    project2 = session['project2']
    project3 = session['project3']
    error = None
    if request.method == 'POST':
        if update_info(request.form['email'],request.form['name'],request.form['bio'],request.form['proj1'],request.form['proj2'],request.form['proj3']):
            return redirect(url_for('logout'))
        else:
            error = 'There was an error in processing your request'

    return render_template('update.html', myName=username, email=email, myBio=bio, myproj1=project1, myproj2=project2, myproj3=project3,error=error)
def update_info(email,username,bio,project1,project2,project3):

    user = User.query.filter(User.email == session['email']).first()
    if isNotBlank(bio) and bio != session['bio']:
        user.bio = bio
        db.session.commit()

    if isNotBlank(email) and email != session['email']:
        user.email = email
        db.session.commit()

    if isNotBlank(username) and username != session['username']:
        user.username = username
        db.session.commit()

    if isNotBlank(project1) and project1 != session['project1']:
        user.project1 = project1
        db.session.commit()

    if isNotBlank(project2) and project2 != session['project2']:
        user.project2 = project2
        db.session.commit()

    if isNotBlank(project3) and project3 != session['project3']:
        user.project3 = project3
        db.session.commit()

    return True




def isNotBlank (myString):
    return (myString and myString.strip())
if __name__ == '__main__':

    app.secret_key = 'A0Zr98j/3yX Z~XHH!lmN]LWX/,?RT'
    app.debug = True
    app.run()
