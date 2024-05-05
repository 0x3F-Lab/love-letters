from flask import Flask, render_template, session, jsonify
from models import db
from config import DevelopmentConfig
import json
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import Post, Notification, User, db, Reply

import random

# Import Blueprints
from blueprints.auth import auth
from blueprints.post import post


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate
    csrf = CSRFProtect(app) # Initialize CSRFProtect

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_message = "You must log in to access this page."
    login_manager.login_message_category = "warning"
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
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
        app.run(debug=True)
