from flask import Flask, render_template, session, jsonify
from models import db
from config import DevelopmentConfig
import json

from models import Post, Notification, User, db

import random

# Import Blueprints
from blueprints.auth import auth
from blueprints.post import post


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Register Blueprints with their URL prefixes
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(post, url_prefix="/post")

    @app.route("/profile/<int:user_id>")
    def user_profile(user_id):
        user = User.query.get_or_404(user_id)
        socials = json.loads(user.socials) if user.socials else {}
        return jsonify(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "socials": socials,
            }
        )

    @app.route("/")
    def home():

        notification_count = 0

        if "user_id" in session:
            user_id = session["user_id"]
            notification_count = Notification.query.filter_by(
                recipient_id=user_id
            ).count()

        return render_template("landing.html", notification_count=notification_count)

    return app


if __name__ == "__main__":
    app = create_app()
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
    posts = Post.query.all()
    return render_template("browse.html", posts=posts)


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
    if "user_id" not in session:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for("home"))

    user_id = session["user_id"]
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("home"))

    return render_template("account_settings.html", user=user)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
