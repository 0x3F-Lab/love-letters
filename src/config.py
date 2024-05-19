import os


class Config:
    # Not utilizing environment variables for key for marking purposes. This is purely demo setup, also repo is public so not safe to upload env
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-key-for-testing")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(Config):
    db_path = os.path.join(os.path.dirname(__file__), "instance", "connect_hearts.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"


# TODO
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    DEBUG = False
