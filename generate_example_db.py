from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os
import random
from src.models import User, Post, Notification, db, Reply
import json

app = Flask(__name__)

project_root = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(project_root, "src", "instance")
if not os.path.exists(instance_path):
    os.makedirs(instance_path, exist_ok=True)

db_path = os.path.join(instance_path, "connect_hearts.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def add_users():
    users_info = [
        {
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice@example.com",
            "password": "password123",
            "gender": "Female",
            "phone_number": "123-456-7890",
            "socials": json.dumps({"instagram": "alice_j"}),
        },
        {
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob@example.com",
            "password": "password123",
            "gender": "Male",
            "phone_number": "987-654-3210",
            "socials": json.dumps({"twitter": "bobsmith", "instagram": "freakyman69"}),
        },
        {
            "first_name": "Carol",
            "last_name": "Martinez",
            "email": "carol@example.com",
            "password": "password123",
            "gender": "Female",
            "phone_number": "555-444-3333",
            "socials": json.dumps({"twitter": "carolm"}),
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
                content=f"Hello I am {user.first_name}. I am so lonely.",
                is_anonymous=random.choice([True, False]),
                post_type=random.choice(
                    ["Love Letter", "Friend Request", "General Broadcast"]
                ),
                created_at=db.func.now(),
            )
            db.session.add(new_post)
    db.session.commit()


def add_notifications():
    users = User.query.all()
    posts = Post.query.all()

    if not users or not posts:
        print("No users or posts available to create notifications.")
        return

    notifications_sent = set()

    for user in users:
        sampled_posts = random.sample(posts, 9)
        for post in sampled_posts:
            if (
                user.user_id,
                post.user_id,
            ) not in notifications_sent and user.user_id != post.user_id:
                notifications_sent.add((user.user_id, post.user_id))
                new_notification = Notification(
                    user_id=user.user_id,
                    recipient_id=post.user_id,
                    post_id=post.post_id,
                    is_read=False,
                    created_at=db.func.now(),
                )
                db.session.add(new_notification)
    db.session.commit()


def add_replies():
    users = User.query.all()
    posts = Post.query.all()

    if not users or not posts:
        print("No users or posts available to create replies.")
        return

    sample_replies = ["Hello Bro :3", "I am also sad :(", "Freak!", "I am oiled up ;)"]

    for post in posts:
        possible_repliers = [user for user in users if user.user_id != post.user_id]
        if not possible_repliers:
            continue
        replier = random.choice(possible_repliers)

        new_reply = Reply(
            post_id=post.post_id,
            user_id=replier.user_id,
            content=random.choice(sample_replies),
            is_anonymous=True,
        )
        db.session.add(new_reply)

    try:
        db.session.commit()
        print("Replies added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding replies: {e}")


def init_db():
    try:
        db.drop_all()
        db.create_all()
        print("Database initialized and tables created.")
    except Exception as e:
        print(f"Error during database initialization: {e}")


def populate_data():
    add_users()
    add_posts()
    add_replies()
    add_notifications()


if __name__ == "__main__":
    with app.app_context():
        init_db()
        populate_data()
