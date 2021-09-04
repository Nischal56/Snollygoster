from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///exams.db' #Can change to MYSQL but preferably not
db = SQLAlchemy(app)

class Exams(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.Text, nullable=False)
    core_subjects = db.Column(db.String(50), nullable=False, default="N/A")
    sub_topics = db.Column(db.String(50), nullable=False, default="N/A")

    def __repr__(self):
        return 'Exam : ' + str(self.id)

class Users(db.Model):                                  #Save the user's data into our own database, for ratings and comfort levels
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.email, nullable=False)
    exam = db.Column(db.String(50), nullable=False)
    favourite = db.Column(db.String(50), nullable=False) #Need to change the datatype, datatype is an input from algorithm

    def __repr__(self):
        return 'User : ' + str(self.id)

class Comfort(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    user_name = db.Column(db.String(50), nullable=False) #Need to link this "User" Table. Have individual comfort tables for each user.
    sub_topics = db.Column(db.Text, nullable=False)
    lvl_of_diff = db.Column(db.String(50), nullable=False, default=5)

    def __repr__(self):
        return 'Comfort Levels : ' + str(self.id)

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    educator_name = db.Column(db.Text, nullable=False, default="N/A")
    agg_rating = db.Column(db.String(50), nullable=False, default=10) #Need to link this as well to the "Users" Table. Have individual ratings table for each user.

    def __repr__(self):
        return 'Rating Details : ' + str(self.id)

class Educators(db.Model):          #Use this class % model to essentially provide educators data and insight when the log in through Google acc.
    id = db.Column(db.Integer, primary_key =True)
    edu_name = db.Column(db.String(50), nullable=False, default="N/A")
    avg_rating = db.Column(db.String(50), nullable=False, default=10)   #This avg rating is compiled by simple mathematical mean.

    def __repr__(self):
        return 'Educator Details : ' + str(self.id)

'''
Retrieve entries in db by Model.query.all() {RETURNS A LIST} {ITERATION THROUGH MODEL.QUERY.ALL()INDEX.COLUMN}
Add data sets to db by db.session.add(Model(Column=...., Column=....))
'''

@app.route('/home', methods=["GET", "POST"])
def home():

    if request.method == 'POST':                    #User information collection
        user_name = request.form['name']
        user_phone = request.form['phone']
        user_email = request.form['email']
        user_exam = request.form['exam']
        user_favedu = request.form['fav']
        new_user = Users(name="user_name", phone="user_phone", email="user_email", exam="user_exam", favourite="user_favedu")
        db.session.add(new_user)
        db.session.commit()
        return redirect('/home')

    else :                                          #Code for displaying the data in the home page only, ie. GET Request


    return render_template('home.html')

@app.route('/comfort', methods=["GET", "POST"])
def comfort():
    return render_template('comfort.html')

@app.route('/phase1', methods=["GET", "POST"])
def phase1():
    return render_template('phase1.html')

@app.route('/phase2', methods=["GET", "POST"])
def phase2():
    return render_template('phase2.html')

@app.route('/phase3', methods=["GET", "POST"])
def phase3():
    return render_template('phase3.html')

@app.route('/tiers')
def tiers():
    return render_template('tiers.html')

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    return render_template('quiz.html')

@app.route('/exams')
def exams():
    return render_template('exams.html', context_manager=context_manager)

context_manager = [

    {"Dummy data 1": "Enter the data for exams or use db data"},
    {"Dummy Data 2": "Enter the data for exams or use db data"}

]

