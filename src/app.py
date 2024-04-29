from flask import Flask, render_template
from flask_migrate import Migrate
from models import db
from config import DevelopmentConfig

# Import Blueprints
from blueprints.auth import auth
from blueprints.post import post


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    migrate = Migrate(app, db)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints with their URL prefixes
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(post, url_prefix="/post")

    @app.route("/")
    def home():
        return render_template("landing.html")

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        app.run()
