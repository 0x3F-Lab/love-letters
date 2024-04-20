from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db
from sqlalchemy.exc import IntegrityError
from flask import jsonify
import re

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
            flash("Successfully logged in", "success")
            return jsonify({'status': 'success', 'message': 'Login successful!'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid email or password.'}), 401

    return render_template("landing.html")




@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))


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

    # Check for non-text characters (allow only alphabetic characters)
    if not re.match(r"^[A-Za-z]+$", value):
        return f"{field_name} should contain only alphabetic characters."
    return None

def validate_email_address(email):
    # Enhanced Basic Format Check with no spaces allowed
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return "Invalid email format."
    return None

def validate_phone_number(phone_number):
    # Check if the phone number contains only digits
    if not phone_number.isdigit():
        return "Phone number should contain only digits."

    # Check for length of the phone number
    if (len(phone_number) < 7 or len(phone_number) > 15):
        return "Phone number should be between 7 and 15 digits."

    return None


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        errors = {}

        # Data fetching
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone_number = request.form.get("phone_number")
        socials = request.form.get("socials")

        # Validation
        if User.query.filter_by(email=email).first():
            errors['email'] = 'Email already exists.'

        errors['email'] = validate_email_address(email) or errors.get('email')
        errors['password'] = validate_password(password)
        errors['first_name'] = validate_text_and_no_spaces(first_name, "First Name")
        errors['last_name'] = validate_text_and_no_spaces(last_name, "Last Name")
        errors['phone_number'] = validate_phone_number(phone_number)

        # Filter out any None values
        errors = {key: val for key, val in errors.items() if val is not None}

        if errors:
            return jsonify({'status': 'error', 'message': errors}), 400

        # Successful validation and user creation
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=generate_password_hash(password),
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
        print(request.form)  # This will show all the data received from the form
        errors = {}

        # Fetching form data
        new_email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        
        # Validate email only if it has been changed
        if new_email != user.email:
            if User.query.filter(User.email == new_email).first():
                errors['email'] = 'This email is already in use.'
            else:
                email_error = validate_email_address(new_email)
                if email_error:
                    errors['email'] = email_error

        errors['phone_number'] = validate_phone_number(phone_number)
        
        # Filter out None values
        errors = {k: v for k, v in errors.items() if v is not None}
        
        print(errors)

        if errors:
            return jsonify({'status': 'error', 'message': errors}), 400

        # If validation passes, update user info
        user.email = new_email
        user.phone_number = phone_number

        try:
            db.session.commit()
            flash("Account details successfully updated", "success")
            return jsonify({'status': 'success', 'message': 'Account updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500

    # Initial page load or GET request
    return render_template("account.html", user=user)


@auth.route("/change_password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        flash("You must be logged in to access this page.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    # Check current password
    if not check_password_hash(user.password_hash, current_password):
        return jsonify({'status': 'error', 'message': 'Current password is incorrect.'}), 400

    # Double confirm new password
    if new_password != confirm_password:
        return jsonify({'status': 'error', 'message': 'New passwords do not match.'}), 400

    # Validate new password
    password_validation_error = validate_password(new_password)
    if password_validation_error:
        return jsonify({'status': 'error', 'message': password_validation_error}), 400

    # Update password hash
    user.password_hash = generate_password_hash(new_password)
    try:
        db.session.commit()
        flash("Password successfully updated", "success")
        return jsonify({'status': 'success', 'message': 'Password updated successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
