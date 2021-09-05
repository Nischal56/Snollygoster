from flask_login import UserMixin
from . import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(500), unique=True, nullable=False)
    order = db.Column(db.String(500), default="NULL")
    # last_watched = db.Column(db.String(500), default="")

class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    importance = db.Column(db.Integer, nullable=False)
    goal = db.Column(db.String(255), nullable=False)
    grade = db.Column(db.Integer)
    prerequisites = db.Column(db.String(255), nullable=False)
