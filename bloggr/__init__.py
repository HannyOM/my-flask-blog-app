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
from flask_migrate import Migrate


db = SQLAlchemy()         # Initializes SQLAlchemy without app.
migrate = Migrate()
bcrypt = Bcrypt()           # Initializes Brcypt without app.
login_manager = LoginManager()          # Initializes Login Manager without app.

def create_app(test_config=None):
    app = Flask(__name__,           # Tells the app the name of the current Python module where it is located.
                instance_relative_config=True)          # Tells the app that the configuration files are relative to the instance folder. 
    app.config.from_mapping(            # Sets some default configurations.
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
    migrate.init_app(app, db)
    bcrypt.init_app(app)            # Initializes Brcypt with app.
    login_manager.init_app(app)         # Initializes Login Manager with app. 
    login_manager.login_view = "auth.login" # type: ignore

    from . import models          # Imports database models.
    
    from . import auth
    app.register_blueprint(auth.auth_bp)            # Registers auth blueprint.

    from .models import User, Post
    @login_manager.user_loader          # Provides a user_loader callback, which reloads the user object from the user ID stored in the session.
    def load_user(user_id):
        return User.query.get(user_id)

    from . import blog
    app.register_blueprint(blog.blog_bp)            # Registers blog blueprint.
    app.add_url_rule("/", endpoint="index")         # Associates the endpoint name "index" with the "/" url so that url_for("index") and url_for("blog.index") will work the same.
    
    return app