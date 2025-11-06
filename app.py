from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bloggr.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    post = db.Column(db.String)
    # author = db.Column(db.String)
    date = db.Column(db.Date)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    all_posts = Post.query.all()
    return render_template("home.html", all_posts=all_posts)


@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("post_title")
    post = request.form.get("post_content")
    if title and post:
        new_post = Post(title=title, post=post, date=datetime.utcnow()) #type: ignore
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    editing_post = Post.query.filter_by(id=post_id).first()
    return render_template("edit.html", editing_post=editing_post)


@app.route("/save/<int:post_id>", methods=["POST"])
def save(post_id):
    editing_post = Post.query.filter_by(id=post_id).first()
    if request.method == "POST":
        new_title = request.form.get("new_post_title")
        new_post = request.form.get("new_post_content")
        if new_title and new_post:
            editing_post.title = new_title
            editing_post.post = new_post
            db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)