from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os
import random

app = Flask(__name__)

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
    gender = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(50))
    socials = db.Column(db.Text)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    post_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


def add_users():
    users_info = [
        {
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice@example.com",
            "password": "password123",
            "gender": "Female",
            "phone_number": "123-456-7890",
            "socials": "instagram: alice_j",
        },
        {
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob@example.com",
            "password": "password123",
            "gender": "Male",
            "phone_number": "987-654-3210",
            "socials": None,
        },
        {
            "first_name": "Carol",
            "last_name": "Martinez",
            "email": "carol@example.com",
            "password": "password123",
            "gender": "Female",
            "phone_number": "555-444-3333",
            "socials": "twitter: carolm",
        },
    ]

    for user_info in users_info:
        hashed_password = generate_password_hash(user_info["password"])
        new_user = User(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            gender=user_info["gender"],
            email=user_info["email"],
            password_hash=hashed_password,
            phone_number=user_info["phone_number"],
            socials=user_info["socials"],
        )
        db.session.add(new_user)
    db.session.commit()


def add_posts():
    users = User.query.all()
    for user in users:
        for i in range(3):
            new_post = Post(
                user_id=user.user_id,
                title=f"{user.first_name}'s Post #{i+1}",
                content=f"Hello I am {user.first_name}. I am so lonely. {'Contact me on ' + user.socials if user.socials else ''}",
                is_anonymous=random.choice([True, False]),
                post_type=random.choice(
                    ["Love Letter", "Friend Request", "General Broadcast"]
                ),
                created_at=db.func.now(),
            )
            db.session.add(new_post)
    db.session.commit()


def init_db():
    db.create_all()
    print("Database initialized and tables created.")


def populate_data():
    add_users()
    add_posts()


if __name__ == "__main__":
    with app.app_context():
        init_db()
        populate_data()
