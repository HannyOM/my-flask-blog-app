from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db, bcrypt
from flask_login import login_user, login_required, logout_user

auth_bp = Blueprint("auth",         # Name of the blueprint.
                    __name__,           # Lets the blueprint know where it is defined.
                    url_prefix="/auth")         # Prepends to all URLs associated to the blueprint

# REGISTER ROUTE
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
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")

# LOGIN ROUTE
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:            
            error = "Username is required."
        elif not password:
            error = "Password is required."
        
        if error is None:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:           # Checks the password hash to verify user.
                hashed_password = existing_user.password
                password_correct = bcrypt.check_password_hash(hashed_password, password)
                if password_correct:
                    login_user(existing_user)
                    return redirect(url_for('hello'))           # TO BE UPDATED
                else:
                    error = "Password is incorrect."
            else:
                error = "Username does not exist."
        flash(error)
    return render_template("auth/login.html")

# LOGOUT ROUTE
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
