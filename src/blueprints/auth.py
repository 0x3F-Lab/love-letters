from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db
from sqlalchemy.exc import IntegrityError
from flask import jsonify

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
        gender = request.form.get("gender")
        phone_number = request.form.get("phone_number")
        socials = request.form.get("socials")

        if User.query.filter_by(email=email).first():
            return jsonify({'status': 'error', 'message': 'Email already exists.'}), 409

        hashed_password = generate_password_hash(password)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hashed_password,
            gender=gender,
            phone_number=phone_number,
            socials=socials,
        )

        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Account successfully created", "success")
            return jsonify({'status': 'success', 'message': 'Account successfully created!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return render_template("landing.html")



@auth.route("/account", methods=["GET", "POST"])
def account():
    if "user_id" not in session:
        flash("You must be logged in to access this page.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        user.email = request.form.get("email", user.email)
        user.first_name = request.form.get("first_name", user.first_name)
        user.last_name = request.form.get("last_name", user.last_name)
        user.gender = request.form.get("gender", user.gender)
        user.phone_number = request.form.get("phone_number", user.phone_number)
        user.socials = request.form.get("socials", user.socials)

        try:
            db.session.commit()
            flash("Account updated successfully!", "success")
        except IntegrityError as e:
            # Prevent an already existing email to be used
            db.session.rollback()
            flash(
                "This email address is already in use. Please choose another one.",
                "danger",
            )
        except Exception as e:
            db.session.rollback()
            flash("An unexpected error occurred. Please try again.", "danger")

    return render_template("account.html", user=user)


@auth.route("/change_password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for("home"))

    user_id = session["user_id"]
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.account"))

    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    # Check current password
    if not check_password_hash(user.password_hash, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("auth.account"))

    # Double confirm new password
    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("auth.account"))

    # Create new password hash and attempt to update database
    user.password_hash = generate_password_hash(new_password)
    try:
        db.session.commit()
        flash("Password updated successfully!", "success")
    except Exception as e:
        # Roll back if database fails to update
        db.session.rollback()
        flash(str(e), "danger")

    return redirect(url_for("auth.account"))
