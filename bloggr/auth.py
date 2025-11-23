from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db, bcrypt

auth_bp = Blueprint("auth",         # Name of the blueprint.
                    __name__,           # Lets the blueprint know where it is defined.
                    url_prefix="/auth",         # Prepends to all URLs associated to the blueprint.
                    template_folder="templates")            # Tells the blueprint where its corresponding Jinja template is located.        

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":            # Gets user's input.
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        
        if not username:            # Ensures user inputted their details.
            error = "Username is required."
        elif not password:
            error = "Password is required."
        
        if error is None:           # Checks database to see if the inputted "username" already exists. 
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                error = "User already exists."
            else:           # Hashes the password and adds it to the database if the username is not already in the database.
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(username=username, password=hashed_password) # type: ignore
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("hello"))           # TO BE CHANGED
        
        flash(error)

    return render_template("auth/register.html")
