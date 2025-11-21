from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db, bcrypt

auth_bp = Blueprint("auth",         # Name of the blueprint.
                    __name__,           # Lets the blueprint know where it is defined.
                    url_prefix="/auth",
                    template_folder="templates")         # Prepends to all URLs associated to the blueprint.

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
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
            if existing_user:
                error = "User already exists."
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(username=username, password=hashed_password) # type: ignore
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("hello"))           # TO BE CHANGED
        
        flash(error)

    return render_template("auth/register.html")
