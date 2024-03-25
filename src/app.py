from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Hard coded for testing
app.config["SECRET_KEY"] = (
    "\xf4\xcdIn\xa0\xabiNZ\x11\x0c\xe5\xa3\x05\xa0AbWs\xfb\xbf3\xb7\x9c"
)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)


def init_db():
    with app.app_context():
        db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user:
            # User exists, check password
            if check_password_hash(user.password_hash, password):
                # Correct password, log in
                return render_template(
                    "status.html", message=f"Logged in account: {username}"
                )
            else:
                flash("Incorrect password. Please try again.")
        else:
            # No user found, create a new account
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return render_template(
                "status.html", message=f"Created account: {username}"
            )
    return render_template("index.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
