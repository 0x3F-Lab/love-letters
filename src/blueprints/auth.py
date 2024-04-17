from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.user_id
            session["user_name"] = f"{user.first_name} {user.last_name}"
            flash("Login successful!", "success")
            return redirect(url_for("post.browse"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("landing.html")


@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.signup"))
        hashed_password = generate_password_hash(password)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account successfully created!", "success")
        return redirect(url_for("auth.login"))
    return render_template("landing.html")


@auth.route("/account", methods=["GET", "POST"])
def account():
    if "user_id" not in session:
        flash("You must be logged in to access this page.", "danger")
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])
    if request.method == "POST":
        user.email = request.form.get("email", user.email)
        user.first_name = request.form.get("first_name", user.first_name)
        user.last_name = request.form.get("last_name", user.last_name)
        db.session.commit()
        flash("Your account has been updated.", "success")
    return render_template("account.html", user=user)


@auth.route("/change_password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        flash("You must be logged in to change your password.", "danger")
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    if check_password_hash(user.password_hash, current_password):
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash("Password successfully changed.", "success")
    else:
        flash("Current password is incorrect.", "danger")
    return redirect(url_for("auth.account"))
