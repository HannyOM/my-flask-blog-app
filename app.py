from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bloggr.sqlite"
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    post = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    date = db.Column(db.Date)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/save", methods=["GET", "POST"])
def save():
    # user clicks add post button
    # if request method is post, 
    # get the value of title
    # get the value of post
    # 
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)