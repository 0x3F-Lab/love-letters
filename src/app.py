from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///connect_hearts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Hard coded for testing
app.config["SECRET_KEY"] = (
    "\xf4\xcdIn\xa0\xabiNZ\x11\x0c\xe5\xa3\x05\xa0AbWs\xfb\xbf3\xb7\x9c"
)

db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(50))
    socials = db.Column(db.Text)

    # Relationships
    posts = db.relationship("Post", backref="author", lazy=True)
    replies = db.relationship("Reply", backref="replier", lazy=True)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship
    replies = db.relationship("Reply", backref="post", lazy=True)


class Reply(db.Model):
    reply_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

@app.route("/create_post", methods=["POST"])
def create_post():
    if request.method == "POST":
        user_id = session.get("user_id")
        if not user_id:
            flash("You need to login to post.", "danger")
            return redirect(url_for("home"))

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

        return redirect(url_for("browse"))

def init_db():
    with app.app_context():
        db.create_all()

@app.route("/", methods=["GET", "POST"])  # Allow both GET and POST requests
def home():

    # Handle Sign Up
    if request.method == "POST" and "signup_form" in request.form:
        # Extract and validate data from the sign-up form
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        gender = request.form.get("gender")  # Optional
        phone_number = request.form.get("phone_number")  # Optional
        socials = request.form.get("socials")  # Optional
        password = request.form.get("password")

        # Assuming you've validated the data
        hashed_password = generate_password_hash(password)

        # Check if email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", "danger")
            return redirect(url_for("home"))

        # Create a new User instance with all collected data
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            gender=gender if gender else None,  # Assign None if empty string
            email=email,
            password_hash=hashed_password,
            phone_number=(
                phone_number if phone_number else None
            ),  # Assign None if empty string
            socials=socials if socials else None,  # Assign None if empty string
        )
        # Add the new user to the database session and commit
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Sign up successful!", "success")
        except Exception as e:
            db.session.rollback()  # Roll back the session on error
            flash(str(e), "danger")

        return redirect(url_for("home"))

    # Handle Login
    elif request.method == "POST" and "login_form" in request.form:
        # Get form data
        email = request.form["email"]
        password = request.form["password"]

        # Check if user exists and the password is correct
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # User exists and password is correct, log them in
            session["user_id"] = user.user_id  # Store user's id in session
            session["user_name"] = (
                f"{user.first_name} {user.last_name}"  # Store user's full name
            )
            flash("Login successful!", "success")
        else:
            # User doesn't exist or password is wrong
            flash("Invalid email or password.", "danger")

    # Render landing.html if it's a GET request or if no form submission occurred
    return render_template("landing.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)  # Remove user_id from session
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@app.route("/browse")
def browse():
    return render_template("browse.html")

@app.route("/post")
def post():
    if "user_id" not in session:
        # redirect to home if not logged in
        flash("You need to be logged in to access this page.", "warning")
        return redirect(url_for("home"))
    return render_template("post.html")

# @app.route("/sign-up")
# def sign_up():
#    return render_template("sign-up.html")

@app.route("/account_settings")
def account_settings():
    return render_template("account_settings.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)