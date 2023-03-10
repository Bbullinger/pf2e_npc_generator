""" Models for NPC app"""
from flask_sqlalchemy import SQLAlchemy
from flask import flask
from flask_bcrypt import Bcrypt
from create_app import app


def connect_db(app):
    db = SQLAlchemy(app)
    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()
        return db


db = connect_db(app)
bcrypt = Bcrypt(app)


class User(db.model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    hashed_password = db.Column(db.Text, nullable=False)

    ########NEED TO IMPLEMENT AUTHENTICATION AND PASSWORD HASHING
    @classmethod
    def encrypt_password(cls, pwd):
        # take the users password, and return an encrypted version
        hashed = bcrypt.generate_password_hash(pwd)

        # need to convert bcrypt's byte string into a utf8 string
        hashed_utf8 = hashed.decode("utf8")
        return hashed_utf8

    @classmethod
    def authenticate(cls, username, pwd):
        """valid user entered credentials. Returns User if match, False otherwise"""

        user = User.query.filter_by(username=username).first()

        # If user exists, and if the hashed version of the user entered password equals
        # the database stored version of user's password match:
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False


class Character(db.Model):
    """Randomized Character"""

    ___tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    background = db.Column(db.Text)
    ancestry = db.Column(db.Text)
    char_class = db.Column(db.Text)

    level = db.Column(db.Text)

    strength = db.Column(db.Integer)
    con = db.Column(db.Integer)
    wis = db.Column(db.Integer)
    dex = db.Column(db.Integer)
    intel = db.Column(db.Integer)
    cha = db.Column(db.Integer)

    ancestry_feats = db.Column(db.Text)
    class_feats = db.Column(db.Text)

    spells = db.Column(db.Text)

    creator = db.relationship(User, backref="character")


class Group(db.Model):
    """Group NPC(s) belong to"""

    __tablename__ = "groups"

    id = db.column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullabe=False)
    character = db.relationship(Character, backref="group")

    creator = db.Column(db.ForeignKey("users.id"), nullable=False)
