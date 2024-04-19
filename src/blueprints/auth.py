from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Notification, db
import json

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
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("landing.html")


@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))


@auth.route('/signup', methods=['POST'])
def signup():
    # Extract data from form submission
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    socials = {
        'instagram': request.form.get('instagram', ''),
        'facebook': request.form.get('facebook', ''),
        'snapchat': request.form.get('snapchat', ''),
        'phone_number': request.form.get('phone_number', '')
    }


    if not any(socials.values()):
        flash("At least one social media handle or phone number must be provided.", "danger")
        return redirect(url_for("auth.login"))

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=generate_password_hash(password),
        socials=json.dumps(socials)  
    )
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        flash("Error creating user", "danger")
        return redirect(url_for("auth.login"))
    
    flash("Account created! You can now login.", "success")

    return redirect(url_for("auth.login"))


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
        user.gender = request.form.get("gender", user.gender)
        user.phone_number = request.form.get("phone_number", user.phone_number)
        user.socials = request.form.get("socials", user.socials)
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


@auth.route("/notifications")
def notifications():
    if 'user_id' not in session:
        flash("You must be logged in to view notifications.", "warning")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_notifications = Notification.query.filter_by(recipient_id=user_id).all()
    return render_template("notifications.html", notifications=user_notifications)

@auth.route('/dismiss_notification/<int:notification_id>', methods=['POST'])
def dismiss_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.recipient_id != session.get('user_id'):
        flash('You do not have permission to delete this notification.', 'danger')
        return redirect(url_for('auth.notifications'))

    db.session.delete(notification)
    db.session.commit()
    flash('Notification dismissed.', 'success')
    return redirect(url_for('auth.notifications'))