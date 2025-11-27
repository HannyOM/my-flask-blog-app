# The functions of this "__init__.py" file are to contain the Application Factory and to tell Python to treat the "Bloggr" directory as a package. 

# Below is an instance of the Flask class created within a function.
# This function is known as the "Application Factory". 
# The Application Factory contains any configuration, registration, or setup the application needs.
# At the end, the app will be returned.

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()         # Initializes SQLAlchemy without app.
bcrypt = Bcrypt()           # Initializes Brcypt without app.
login_manager = LoginManager()          # Initializes Login Manager without app.

def create_app(test_config=None):
    app = Flask(__name__,           # Tells the app the name of the current Python module where it is located.
                instance_relative_config=True)          # Tells the app that the configuration files are relative to the instance folder. 
    app.config.from_mapping(            # Sets some default configurations.
        SECRET_KEY = "mydev",
        SQLALCHEMY_DATABASE_URI = os.path.join("sqlite:///" + app.instance_path, "bloggr.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)            # Loads the instance configurations, if it exists, when not in testing.
    else:
        app.config.from_mapping(test_config)            # Loads the test configurations if passed in, when in testing.

    try:
        os.makedirs(app.instance_path)          # Attempts to create an instance path if one doesn't already exist.
    except OSError:
        pass

    db.init_app(app)            # Initializes SQLAlchemy with app.
    bcrypt.init_app(app)            # Initializes Brcypt with app.
    login_manager.init_app(app)         # Initializes Login Manager with app.        
 
    from . import models          # Imports database models.

    with app.app_context():         # Creates database tables.
        db.create_all()

    from . import auth          # Imports auth blueprint.
    app.register_blueprint(auth.auth_bp)            # Registers auth blueprint.

    from .models import User
    @login_manager.user_loader          # Provides a user_loader callback, which reloads the user object from the user ID stored in the session.
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/hello")
    def hello():
        return "Hello Hanny"
    
    return app



























































































# from flask import Flask, render_template, redirect, url_for, request
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime


# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bloggr.sqlite"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String)
#     post = db.Column(db.String)
#     # author = db.Column(db.String)
#     date = db.Column(db.Date)

# with app.app_context():
#     db.create_all()

# @app.route("/")
# def home():
#     all_posts = Post.query.all()
#     return render_template("home.html", all_posts=all_posts)


# @app.route("/new")
# def new():
#     return render_template("new.html")


# @app.route("/add", methods=["POST"])
# def add():
#     title = request.form.get("post_title")
#     post = request.form.get("post_content")
#     if title and post:
#         new_post = Post(title=title, post=post, date=datetime.utcnow()) #type: ignore
#         db.session.add(new_post)
#         db.session.commit()
#     return redirect(url_for("home"))


# @app.route("/edit/<int:post_id>", methods=["GET", "POST"])
# def edit(post_id):
#     editing_post = Post.query.filter_by(id=post_id).first()
#     return render_template("edit.html", editing_post=editing_post)


# @app.route("/save/<int:post_id>", methods=["POST"])
# def save(post_id):
#     editing_post = Post.query.filter_by(id=post_id).first()
#     if request.method == "POST":
#         new_title = request.form.get("new_post_title")
#         new_post = request.form.get("new_post_content")
#         if new_title and new_post:
#             editing_post.title = new_title
#             editing_post.post = new_post
#             db.session.commit()
#     return redirect(url_for("home"))


# if __name__ == "__main__":
#     app.run(debug=True)