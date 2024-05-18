from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from models import LikePost, LikeReply, Post, Reply, User, Notification, db
from sqlalchemy.exc import IntegrityError
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
    login_required,
)
from sqlalchemy import case


post = Blueprint("post", __name__)


@post.route("/create_post", methods=["POST"])
def create_post():
    if request.method == "POST":

        if not current_user.is_authenticated:
            flash("You need to login to post.", "danger")
            return redirect(url_for("home"))

        title = request.form.get("title")
        content = request.form.get("content")
        post_type = request.form.get("post_type")
        is_anonymous = "is_anonymous" in request.form

        new_post = Post(
            user_id=current_user.user_id,
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
@login_required
def create():
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(
            recipient_id=current_user.user_id
        ).count()
    return render_template("post.html", notification_count=notification_count)


from sqlalchemy import case


@post.route("/browse")
@post.route("/browse/<int:page>")
def browse(page=1):
    sort_option = request.args.get("sort", "newest")
    per_page = 10

    # Count number of likes each post has
    likes_count_subq = (
        db.session.query(
            LikePost.post_id, db.func.count(LikePost.post_id).label("like_count")
        )
        .group_by(LikePost.post_id)
        .subquery()
    )

    # Query all posts even those with no likes (use of outerjoin)
    base_query = db.session.query(Post).outerjoin(
        likes_count_subq, likes_count_subq.c.post_id == Post.post_id
    )

    # Determine sorting based on the option
    if sort_option == "oldest":
        sort_criteria = Post.created_at.asc()
    elif sort_option == "most_liked":
        sort_criteria = db.desc(likes_count_subq.c.like_count)
    elif sort_option == "least_liked":
        sort_criteria = likes_count_subq.c.like_count
    elif sort_option.startswith("type_"):
        post_type = sort_option.split("_")[1]
        type_sort = case((Post.post_type == post_type, 0), else_=1)
        base_query = base_query.order_by(type_sort, Post.created_at.desc())
    else:
        sort_criteria = Post.created_at.desc()

    if not sort_option.startswith("type_"):
        base_query = base_query.order_by(sort_criteria)

    posts = base_query.paginate(page=page, per_page=per_page, error_out=False)

    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        posts_html = render_template("posts_list.html", posts=posts.items, user=user)
        return jsonify({"posts": posts_html, "has_next": posts.has_next})

    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(
            recipient_id=current_user.user_id
        ).count()

    return render_template(
        "browse.html",
        posts=posts.items,
        user=user,
        notification_count=notification_count,
    )


@post.route("/like_post", methods=["POST"])
def like_post():
    if not current_user.is_authenticated:
        return jsonify({"error": "You need to log in to like posts"}), 403

    post_id = request.form.get("post_id")
    user_id = request.form.get("user_id")
    like = LikePost.query.filter_by(
        user_id=current_user.user_id, post_id=post_id
    ).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify(
            {
                "status": "like",
                "count": LikePost.query.filter_by(post_id=post_id).count(),
            }
        )
    else:
        new_like = LikePost(user_id=current_user.user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify(
            {
                "status": "unlike",
                "count": LikePost.query.filter_by(post_id=post_id).count(),
            }
        )


@post.route("/like_reply", methods=["POST"])
def like_reply():
    if not current_user.is_authenticated:
        return jsonify({"error": "You need to log in to like replies"}), 403

    reply_id = request.form.get("reply_id")
    user_id = request.form.get("user_id")
    like = LikeReply.query.filter_by(
        user_id=current_user.user_id, reply_id=reply_id
    ).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        new_count = LikeReply.query.filter_by(reply_id=reply_id).count()
        return jsonify({"status": "like", "count": new_count})
    else:
        new_like = LikeReply(user_id=current_user.user_id, reply_id=reply_id)
        db.session.add(new_like)
        db.session.commit()
        new_count = LikeReply.query.filter_by(reply_id=reply_id).count()
        return jsonify({"status": "unlike", "count": new_count})


@post.route("/submit_reply", methods=["POST"])
def submit_reply():
    # Check if the user is authenticated
    if not current_user.is_authenticated:
        return jsonify({"error": "You need to log in to reply"}), 403

    post_id = request.form["post_id"]
    content = request.form["content"]
    is_anonymous = (
        "is_anonymous" in request.form
    )  # Check if the checkbox for anonymous was checked

    new_reply = Reply(
        post_id=post_id,
        user_id=current_user.user_id,  # Now safe to access, as we've checked authentication
        content=content,
        is_anonymous=is_anonymous,
    )
    db.session.add(new_reply)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": "Reply posted successfully!",
                "post_id": post_id,
                "content": content,
                "anonymous": is_anonymous,
            }
        )
    except Exception as e:
        # Log the exception to the console
        print("Error submitting reply:", e)
        db.session.rollback()  # Rollback any changes made before the error occurred
        return jsonify({"error": "An error occurred while submitting the reply"}), 500


@post.route("/connect/<int:post_id>", methods=["POST"])
def connect(post_id):

    if not current_user.is_authenticated:
        flash("You need to login to connect.", "danger")
        return redirect(url_for("post.browse"))

    post = Post.query.get_or_404(post_id)
    recipient_id = post.user_id

    # Check if the current user is trying to connect with themselves
    if current_user.user_id == recipient_id:
        flash("You cannot connect with yourself.", "info")
        return redirect(url_for("post.browse"))

    # Check for existing notification to avoid duplicate requests
    existing_notification = Notification.query.filter_by(
        user_id=current_user.user_id, recipient_id=recipient_id
    ).first()

    if existing_notification:
        flash("You have already sent a connection request to this user.", "info")
        return redirect(url_for("post.browse"))

    # Create and save a new notification
    new_notification = Notification(
        user_id=current_user.user_id, recipient_id=recipient_id, post_id=post_id
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
