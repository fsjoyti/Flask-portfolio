from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request , redirect
from flask import  url_for
from flask import session




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
    user = User.query.filter(User.email==email, User.password==password)
    if user is None:
        return False
    else:
        session["username"]= user.username
        session["email"]=user.email
        session ["bio"]=user.bio
        session["project1"] = user.project1
        session["project2"]= user.project2
        session["project3"] = user.project3


        return True

@app.route('/profile', methods=['GET'])
def log_the_user_in():
    email = session['email']
    return render_template('profile.html',email =email)












if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX Z~XHH!lmN]LWX/,?RT'
    app.debug = True
    app.run()
