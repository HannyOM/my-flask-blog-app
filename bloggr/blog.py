from flask import Blueprint, render_template, request, redirect, url_for
from .models import Post
from . import db
from datetime import datetime

blog_bp = Blueprint('blog',         # Name of the blueprint.
                    __name__)           # Lets the blueprint know where it is defined.

@blog_bp.route("/")
def index():
    all_posts = Post.query.all()
    return render_template("blog/index.html", all_posts=all_posts)

@blog_bp.route("/new")
def new():
    return render_template("blog/new.html")

@blog_bp.route("/add", methods=["POST"])
def add():
    title = request.form.get("post_title")
    content = request.form.get("post_content")
    if title and content:
        new_content = Post(title=title, content=content, date=datetime.utcnow()) #type: ignore
        db.session.add(new_content)
        db.session.commit()
    return redirect(url_for("blog.index"))

@blog_bp.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    editing_post = Post.query.filter_by(id=post_id).first()
    return render_template("blog/edit.html", editing_post=editing_post)

@blog_bp.route("/save/<int:post_id>", methods=["POST"])
def save(post_id):
    editing_post = Post.query.filter_by(id=post_id).first()
    if request.method == "POST":
        new_title = request.form.get("new_post_title")
        new_post = request.form.get("new_post_content")
        if new_title and new_post:
            editing_post.title = new_title # type: ignore
            editing_post.content = new_post # type: ignore
            db.session.commit()
    return redirect(url_for("blog.index"))

@blog_bp.route("/delete/<int:post_id>", methods=["GET"])
def delete(post_id):
    deleting_post = Post.query.filter_by(id=post_id).first()
    db.session.delete(deleting_post)
    db.session.commit()
    return redirect(url_for("blog.index"))