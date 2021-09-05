from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    name = request.form.get('full_name') 
    password = "Password"

    userExists = Users.query.filter_by(username=username).first()

    if userExists:
        user = Users.query.filter_by(username=username).first()
        login_user(user, remember=True)
        print(user)
        return redirect('/dashboard')

    
    new_user = Users(username=username, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    print("User added:", new_user.username, new_user.password)
    
    user = Users.query.filter_by(username=username).first()
    
    print(user)

    return redirect('/personalise')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))