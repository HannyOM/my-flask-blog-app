from flask import Blueprint 

auth_bp = Blueprint("auth",         # Name of the blueprint.
                    __name__,           # Lets the blueprint know where it is defined.
                    url_prefix="/auth")         # Prepends to all URLs associated to the blueprint.

@auth_bp.route("/register")
def register():
    return "Registration Page"
