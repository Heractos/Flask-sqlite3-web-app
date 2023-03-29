from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Post, Comment, Like, User
from sqlalchemy.sql import func
from markupsafe import Markup
from . import db

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        title = request.form.get("title")
        content = Markup(request.form.get("content"))
        if not title or not content:
            flash("Please enter a title and content for your post", category="error")
        else:
            post = Post(title=title, content=content, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")
            return redirect(url_for("views.index"))

    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("index.html", posts=posts, safe=func.safe)


@views.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = Markup(request.form.get("content"))
        post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("views.index"))
    return render_template("create_post.html", title="Create Post")


@views.route("/like_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(post_id=post.id, user_id=current_user.id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash("Your like has been removed!", "success")
    else:
        like = Like(post_id=post.id, user_id=current_user.id)
        db.session.add(like)
        db.session.commit()
        flash("Your like has been added!", "success")
    return redirect(url_for("views.index"))


@views.route("/comment_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get("content")
    comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
    db.session.add(comment)
    db.session.commit()
    flash("Your comment has been added!", "success")
    return redirect(url_for("views.index"))


@views.route("/delete_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash("You are not authorized to delete this post!", "danger")
        return redirect(url_for("views.index"))
    comments = Comment.query.filter_by(post_id=post_id).all()
    for comment in comments:
        db.session.delete(comment)
    likes = Like.query.filter_by(post_id=post_id).all()
    for like in likes:
        db.session.delete(like)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("views.index"))
