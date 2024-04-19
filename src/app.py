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

    @app.route('/profile/<int:user_id>')
    def user_profile(user_id):
        user = User.query.get_or_404(user_id)
        socials = json.loads(user.socials) if user.socials else {}
        return jsonify({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'socials': socials
        })

    @app.route("/")
    def home():
        love_letters = Post.query.all()
        random_letter = random.choice(love_letters) if love_letters else None

        notification_count = 0
        
        if 'user_id' in session:
            user_id = session['user_id']
            notification_count = Notification.query.filter_by(recipient_id=user_id).count()

        return render_template("landing.html", random_letter=random_letter, notification_count=notification_count)
    
    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        app.run()
