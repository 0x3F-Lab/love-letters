from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(50))
    socials = db.Column(JSON)

    # Relationships
    posts = db.relationship("Post", backref="author", lazy=True)
    replies = db.relationship("Reply", backref="replier", lazy=True)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    title = db.Column(db.String(200), nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship
    replies = db.relationship("Reply", backref="post", lazy=True, order_by="desc(Reply.created_at)")



class Reply(db.Model):
    reply_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship(
        "User",
        backref=db.backref("sent_notifications", lazy="dynamic"),
        foreign_keys=[user_id],
    )
    recipient = db.relationship(
        "User",
        backref=db.backref("received_notifications", lazy="dynamic"),
        foreign_keys=[recipient_id],
    )
    post = db.relationship("Post")

    __table_args__ = (
        db.UniqueConstraint("user_id", "recipient_id", name="_user_recipient_uc"),
    )
