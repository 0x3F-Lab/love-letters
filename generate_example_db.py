from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os
import random
import json
from src.models import User, Post, Notification, db, Reply, LikePost, LikeReply

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
            "socials": json.dumps({"instagram": "alice_j", "snapchat": "alice_j"}),
        },
        {
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob@example.com",
            "password": "password123",
            "gender": "Male",
            "phone_number": "987-654-3210",
            "socials": json.dumps({"facebook": "bobsmith", "instagram": "freakyman69"}),
        },
        {
            "first_name": "Carol",
            "last_name": "Martinez",
            "email": "carol@example.com",
            "password": "password123",
            "gender": "Female",
            "phone_number": "555-444-3333",
            "socials": json.dumps({"instagram": "carolm"}),
        },
        {
            "first_name": "David",
            "last_name": "Brown",
            "email": "david@example.com",
            "password": "password123",
            "gender": "Male",
            "phone_number": "444-555-6666",
            "socials": json.dumps({"facebook": "david_b"}),
        },
        {
            "first_name": "Eve",
            "last_name": "Davis",
            "email": "eve@example.com",
            "password": "password123",
            "gender": "Female",
            "phone_number": "333-222-1111",
            "socials": json.dumps({"snapchat": "eve_d"}),
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
    sample_posts = [
        "Every moment with you feels like a beautiful dream.",
        "I've never felt this way before; you make my heart race.",
        "Your smile is my favorite thing in the world.",
        "I can't stop thinking about you; you're always on my mind.",
        "My love for you grows stronger every day.",
        "I cherish every moment we spend together.",
        "You're my soulmate, my everything.",
        "I love you more than words can say.",
        "You light up my life in ways I never thought possible.",
        "I am so grateful to have you in my life.",
    ]

    for user in users:
        for i in range(5):
            new_post = Post(
                user_id=user.user_id,
                title=f"{user.first_name}'s Love Letter #{i+1}",
                content=random.choice(sample_posts)
                + " "
                + random.choice(sample_posts)
                + " "
                + random.choice(sample_posts),
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

    sample_replies = [
        "Hello Bro :3",
        "I am also sad :(",
        "I am oiled up ;)",
        "That's so sweet!",
        "I feel the same way.",
        "Thank you for sharing this.",
        "This made my day better.",
        "You're amazing!",
        "Let's talk more.",
    ]

    for post in posts:
        for i in range(random.randint(1, 5)):
            possible_repliers = [user for user in users if user.user_id != post.user_id]
            if not possible_repliers:
                continue
            replier = random.choice(possible_repliers)

            new_reply = Reply(
                post_id=post.post_id,
                user_id=replier.user_id,
                content=random.choice(sample_replies) + " "
                + random.choice(sample_replies) + " "
                + random.choice(sample_replies),
                is_anonymous=random.choice([True, False]),
            )
            db.session.add(new_reply)

    try:
        db.session.commit()
        print("Replies added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding replies: {e}")


def add_likes():
    users = User.query.all()
    posts = Post.query.all()
    replies = Reply.query.all()

    for post in posts:
        for _ in range(random.randint(0, len(users))):
            user = random.choice(users)
            if not LikePost.query.filter_by(
                user_id=user.user_id, post_id=post.post_id
            ).first():
                new_like_post = LikePost(user_id=user.user_id, post_id=post.post_id)
                db.session.add(new_like_post)

    for reply in replies:
        for _ in range(random.randint(0, len(users))):
            user = random.choice(users)
            if not LikeReply.query.filter_by(
                user_id=user.user_id, reply_id=reply.reply_id
            ).first():
                new_like_reply = LikeReply(
                    user_id=user.user_id, reply_id=reply.reply_id
                )
                db.session.add(new_like_reply)

    try:
        db.session.commit()
        print("Likes added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding likes: {e}")


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
    add_likes()


if __name__ == "__main__":
    with app.app_context():
        init_db()
        populate_data()
