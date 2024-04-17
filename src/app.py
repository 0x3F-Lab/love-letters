from flask import Flask, render_template
from models import db
from config import DevelopmentConfig

from models import Post, db

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

    @app.route("/")
    def home():
        love_letters = Post.query.all()
        random_letter = random.choice(love_letters)
        return render_template("landing.html", random_letter=random_letter)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        app.run()
