from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import random
import datetime
import os

project_root = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(project_root, "src", "instance")
if not os.path.exists(instance_path):
    os.makedirs(instance_path, exist_ok=True)

db_path = os.path.join(instance_path, "connect_hearts.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)


def add_users():
    users_info = [
        {
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice@example.com",
            "password": "password123",
            "socials": "instagram: example",
        },
        {
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob@example.com",
            "password": "password123",
        },
        {
            "first_name": "Carol",
            "last_name": "Martinez",
            "email": "carol@example.com",
            "password": "password123",
            "socials": "onlyfans: cheeky",
        },
    ]
    for user_info in users_info:
        hashed_password = generate_password_hash(user_info["password"])
        new_user = User(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            email=user_info["email"],
            password_hash=hashed_password,
        )
        db.session.add(new_user)
    db.session.commit()


def add_posts():
    users = User.query.all()
    for user in users:
        for i in range(3):
            new_post = Post(
                user_id=user.user_id,
                title=f"Hello this is my {i+1}st post! I am lonely. ",
                content=f"I am {user.first_name} and I am so lonely. Please message me {user.socials}",
            )
            db.session.add(new_post)
    db.session.commit()


def init_db():
    print(f"Creating the database at {db_path}...")
    db.create_all()
    print("Database created.")


def populate_data():
    add_users()
    add_posts()


if __name__ == "__main__":
    with app.app_context():
        init_db()
        populate_data()
