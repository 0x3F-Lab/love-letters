from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Notification, db
from sqlalchemy.exc import IntegrityError
from flask import jsonify
import re
import json
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
    login_required,
)

auth = Blueprint("auth", __name__)

# Validation Functions


def validate_password(password):
    if " " in password:
        return "Password should not contain spaces."
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search("[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search("[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search("[0-9]", password):
        return "Password must contain at least one number."
    if not re.search("[!@#$%^&*]", password):
        return "Password must contain at least one special character."

    # Check for invalid characters (any characters other than letters, numbers, and specified special characters)
    if re.search("[^a-zA-Z0-9!@#$%^&*]", password):
        return "Invalid character detected. Only letters, numbers, and !@#$%^&* are allowed."

    return None


def validate_text_and_no_spaces(value, field_name):
    # Check for spaces
    if " " in value:
        return f"{field_name} should not contain spaces."

    # Check for non-text characters (allow only alphabetic characters as well as names with an apostrophe)
    if not re.match(r"^[A-Za-z']+$", value):
        return f"{field_name} should contain only alphabetic characters."
    return None


def validate_email_address(email):
    # Enhanced Basic Format Check with no spaces allowed
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return "Invalid email format."
    return None


def validate_phone_number(phone_number):
    # Return None if phone_number not provided
    if phone_number == "":
        return None

    # Strip out '+' and '-' for validation
    cleaned_number = phone_number.replace("-", "").replace("+", "")

    # Check if the stripped phone number contains only digits
    if not cleaned_number.isdigit():
        return "Phone number should contain only digits, '+' or '-'."

    # Check for correct length
    if len(cleaned_number) < 7 or len(cleaned_number) > 15:
        return "Phone number should be between 7 and 15 digits."

    return None


def validate_socials(value, social_handle):
    if value == "":
        return None

    if social_handle == "facebook":
        if not re.match(r"https?://www\.facebook\.com/.+", value):
            return "Please enter a valid Facebook URL"

    if social_handle == "instagram":
        if not re.match(r"^[a-zA-Z0-9._]{1,30}$", value):
            return "Please enter a valid Instagram username"

    if social_handle == "snapchat":
        if not re.match(r"^[a-zA-Z0-9]{3,15}$", value):
            return "Please eneter a valid snapchat username"

    return None


# ----- Form Processing -----

# Sign-up


@auth.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":

        print("Method called")

        errors = {}

        # Data fetching
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        gender = request.form.get("gender")
        email = request.form.get("email").lower()
        password = request.form.get("password")
        phone_number = request.form.get("phone_number", "")
        socials = {
            "instagram": request.form.get("instagram", ""),
            "facebook": request.form.get("facebook", ""),
            "snapchat": request.form.get("snapchat", ""),
        }

        if not any(socials.values()):
            errors["socials"] = "At least one social media handle must be provided"

        if User.query.filter_by(email=email).first():
            errors["email"] = "Email already exists."

        errors["email"] = validate_email_address(email) or errors.get("email")
        errors["password"] = validate_password(password)
        errors["first_name"] = validate_text_and_no_spaces(first_name, "First Name")
        errors["last_name"] = validate_text_and_no_spaces(last_name, "Last Name")
        errors["phone_number"] = validate_phone_number(phone_number)

        for platform, username in socials.items():
            errors[platform] = validate_socials(username, platform)

        # Filter out any None values
        errors = {key: val for key, val in errors.items() if val is not None}

        print(errors)

        if errors:
            return jsonify({"status": "error", "message": errors}), 400

        # Successful validation and user creation

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            password_hash=generate_password_hash(password),
            phone_number=phone_number,
            socials=json.dumps(socials),
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Account successfully created", "success")
            return jsonify(
                {"status": "success", "message": "Account successfully created!"}
            )
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    return render_template("landing.html")


# Update user information


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():

    user = current_user

    if not current_user.is_authenticated:
        flash("User not found.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        # print(request.form) debugging
        errors = {}

        # Fetching form data
        new_email = request.form.get("email").lower()
        phone_number = request.form.get("phone_number")
        gender = request.form.get("gender")
        phone_number = request.form.get("phone_number", "")
        socials = {
            "instagram": request.form.get("instagram", ""),
            "facebook": request.form.get("facebook", ""),
            "snapchat": request.form.get("snapchat", ""),
        }

        # Validate email only if it has been changed
        if new_email != user.email:
            if User.query.filter(User.email == new_email).first():
                errors["email"] = "This email is already in use."
            else:
                email_error = validate_email_address(new_email)
                if email_error:
                    errors["email"] = email_error

        if not any(socials.values()):
            errors["missingSocialError"] = (
                "At least one social media handle must be provided"
            )

        errors["phone_number"] = validate_phone_number(phone_number)

        for platform, username in socials.items():
            errors[platform] = validate_socials(username, platform)

        # Filter out None values
        errors = {k: v for k, v in errors.items() if v is not None}

        # print(errors) debugging

        if errors:
            return jsonify({"status": "error", "message": errors}), 400

        # If validation passes, update user info
        user.email = new_email
        user.phone_number = phone_number
        user.gender = gender
        user.socials = json.dumps(socials)

        try:
            db.session.commit()
            flash("Account details successfully updated", "success")
            return (
                jsonify(
                    {"status": "success", "message": "Account updated successfully!"}
                ),
                200,
            )
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    if user.socials:
        socials = json.loads(user.socials)
        user.instagram = socials.get("instagram", "")
        user.facebook = socials.get("facebook", "")
        user.snapchat = socials.get("snapchat", "")

    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(
            recipient_id=current_user.user_id
        ).count()

    # Initial page load or GET request
    return render_template(
        "account.html", user=user, notification_count=notification_count
    )


# Update account password


@auth.route("/change_password", methods=["POST"])
@login_required
def change_password():

    user = current_user

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("home"))

    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    # Check current password
    if not check_password_hash(user.password_hash, current_password):
        return (
            jsonify({"status": "error", "message": "Current password is incorrect."}),
            400,
        )

    # Double confirm new password
    if new_password != confirm_password:
        return (
            jsonify({"status": "error", "message": "New passwords do not match."}),
            400,
        )

    # Validate new password
    password_validation_error = validate_password(new_password)
    if password_validation_error:
        return jsonify({"status": "error", "message": password_validation_error}), 400

    # Update password hash
    user.password_hash = generate_password_hash(new_password)
    try:
        db.session.commit()
        flash("Password successfully updated", "success")
        return (
            jsonify({"status": "success", "message": "Password updated successfully!"}),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# Log-in


@auth.route("/login", methods=["GET", "POST"])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('auth.'))  # Redirect if already logged in

    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Successfully logged in", "success")
            return jsonify({"status": "success", "message": "Login successful!"}), 200
        else:
            return (
                jsonify({"status": "error", "message": "Invalid email or password."}),
                401,
            )

    return render_template("landing.html")


# Logout


@auth.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


# Notifications


@auth.route("/notifications")
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(
        recipient_id=current_user.get_id()
    ).all()

    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(
            recipient_id=current_user.user_id
        ).count()

    return render_template(
        "notifications.html",
        notifications=user_notifications,
        notification_count=notification_count,
    )


@auth.route("/dismiss_notification/<int:notification_id>", methods=["POST"])
def dismiss_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if str(notification.recipient_id) != current_user.get_id():
        flash("You do not have permission to delete this notification.", "danger")
        return redirect(url_for("auth.notifications"))

    db.session.delete(notification)
    db.session.commit()
    flash("Notification dismissed.", "success")

    return redirect(url_for("auth.notifications"))
