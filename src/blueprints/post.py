
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import Post, Reply, User, Notification, db
from sqlalchemy.exc import IntegrityError



post = Blueprint("post", __name__)


@post.route("/create_post", methods=["POST"])
def create_post():
    if request.method == "POST":
        user_id = session.get("user_id")
        if not user_id:
            flash("You need to login to post.", "danger")
            return redirect(url_for("auth.login"))

        title = request.form.get("title")
        content = request.form.get("content")
        post_type = request.form.get("post_type")
        is_anonymous = "is_anonymous" in request.form

        new_post = Post(
            user_id=user_id,
            title=title,
            content=content,
            post_type=post_type,
            is_anonymous=is_anonymous,
        )

        db.session.add(new_post)
        try:
            db.session.commit()
            flash("Post created successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(str(e), "danger")

        posts = Post.query.all()
        for post in posts:
            # some debugging stuff
            print(
                f"ID: {post.post_id}, Title: {post.title}, Content: {post.content}, Type: {post.post_type}, Poster: {post.user_id}, Anonymous: {post.is_anonymous}, Time: {post.created_at}"
            )

        return redirect(url_for("post.browse"))


@post.route("/create")
def create():
    user_id = session.get("user_id")
    if not user_id:
        flash("You need to login to post.", "danger")
        return redirect(url_for("auth.login"))
    return render_template("post.html")


@post.route("/browse")
def browse():
    posts = Post.query.options(db.joinedload(Post.replies)).all()
    return render_template("browse.html", posts=posts)




@post.route('/submit_reply', methods=['POST'])
def submit_reply():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You need to log in to reply"}), 403

    post_id = request.form['post_id']
    content = request.form['content']
    new_reply = Reply(post_id=post_id, user_id=user_id, content=content)
    db.session.add(new_reply)

    try:
        db.session.commit()
        return jsonify({"message": "Reply posted successfully!", "post_id": post_id, "content": content})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@post.route("/connect/<int:post_id>", methods=["POST"])
def connect(post_id):
    if "user_id" not in session:
        flash("You need to log in to connect.", "danger")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    post = Post.query.get_or_404(post_id)
    recipient_id = post.user_id

    if user_id == recipient_id:
        flash("You cannot connect with yourself.", "info")
        return redirect(url_for("post.browse"))

    existing_notification = Notification.query.filter_by(
        user_id=user_id, recipient_id=recipient_id
    ).first()

    if existing_notification:
        flash("You have already sent a connection request to this user.", "info")
        return redirect(url_for("post.browse"))

    new_notification = Notification(
        user_id=user_id, recipient_id=recipient_id, post_id=post_id
    )
    db.session.add(new_notification)
    try:
        db.session.commit()
        flash("Connect request sent.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(
            "Connection request failed. You may have already connected to this user.",
            "info",
        )

    return redirect(url_for("post.browse"))

