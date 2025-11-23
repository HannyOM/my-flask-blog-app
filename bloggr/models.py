from . import db
from flask_login import UserMixin

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    date = db.Column(db.Date)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
