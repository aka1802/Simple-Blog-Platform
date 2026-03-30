from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from . import db
from .models import User, Post, Comment, Like, Dislike
import os
from werkzeug.utils import secure_filename

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    search_query = request.args.get('search')
    
    if search_query:
        
        posts = Post.query.join(User).filter(
            User.username.contains(search_query)
        ).order_by(Post.date_created.desc()).all()
        
        if not posts:
            flash(f'No posts found from user "{search_query}"', category='error')
    else:
        posts = Post.query.order_by(Post.date_created.desc()).all()
        
    return render_template("home.html", user=current_user, posts=posts, search_query=search_query)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        category = request.form.get('category')
        file = request.files.get('image')
        if not text:
            flash('Post cannot be empty!', category='error')
        else:
            filename = None
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            new_post = Post(text=text, category=category, image=filename, author=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template("create_post.html", user=current_user)

@views.route("/profile/<username>")
@login_required
def profile(username):
    user_to_show = User.query.filter_by(username=username).first()
    if not user_to_show:
        flash("User not found.", category="error")
        return redirect(url_for("views.home"))
    return render_template("profile.html", user=current_user, profile_user=user_to_show)

@views.route("/follow/<username>")
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    if user_to_follow and user_to_follow != current_user:
        current_user.followed.append(user_to_follow)
        db.session.commit()
    return redirect(url_for('views.profile', username=username))

@views.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user_to_unfollow = User.query.filter_by(username=username).first()
    if user_to_unfollow:
        current_user.followed.remove(user_to_unfollow)
        db.session.commit()
    return redirect(url_for('views.profile', username=username))

@views.route("/followers/<username>")
@login_required
def followers_list(username):
    user_to_show = User.query.filter_by(username=username).first()
    return render_template("followers.html", user=current_user, profile_user=user_to_show)

@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.get(post_id)
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    dislike = Dislike.query.filter_by(author=current_user.id, post_id=post_id).first()
    if dislike: db.session.delete(dislike)
    if like: db.session.delete(like)
    else: db.session.add(Like(author=current_user.id, post_id=post_id))
    db.session.commit()
    return jsonify({"likes": len(post.likes), "dislikes": len(post.dislikes)})

@views.route("/dislike-post/<post_id>", methods=['POST'])
@login_required
def dislike(post_id):
    post = Post.query.get(post_id)
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    dislike = Dislike.query.filter_by(author=current_user.id, post_id=post_id).first()
    if like: db.session.delete(like)
    if dislike: db.session.delete(dislike)
    else: db.session.add(Dislike(author=current_user.id, post_id=post_id))
    db.session.commit()
    return jsonify({"likes": len(post.likes), "dislikes": len(post.dislikes)})

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if text:
        db.session.add(Comment(text=text, author=current_user.id, post_id=post_id))
        db.session.commit()
    return redirect(url_for('views.home'))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment and (current_user.id == comment.author or current_user.id == comment.post.author):
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('views.home'))

@views.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        current_user.bio = request.form.get("bio")
        file = request.files.get("profile_pic")
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_pic = filename
        db.session.commit()
        return redirect(url_for("views.profile", username=current_user.username))
    return render_template("edit_profile.html", user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if post and post.author == current_user.id:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("views.home"))