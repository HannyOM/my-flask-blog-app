from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):            # Initializes a "User" table with three columns.
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)            # Creates a relationship to the Post model so a user can have many posts.

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)            # Initializes a "Post" table with five columns.
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) # "ForeignKey" points to the "id" column in the "User" table.
    date = db.Column(db.Date)



