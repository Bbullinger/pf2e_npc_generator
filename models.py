""" Models for NPC app"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from create_app import app


def connect_db(app):
    db = SQLAlchemy()
    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()
        return db


db = connect_db(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)

    ########NEED TO IMPLEMENT AUTHENTICATION AND PASSWORD HASHING
    @classmethod
    def signup(cls, username, password, email):
        # take the users password, and return an encrypted version
        hashed = bcrypt.generate_password_hash(password)

        # need to convert bcrypt's byte string into a utf8 string
        hashed_utf8 = hashed.decode("utf8")
        user = User(username=username, password=hashed_utf8, email=email)
        db.session.add(user)
        return user

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

    level = db.Column(db.Integer)

    strength = db.Column(db.Integer)
    con = db.Column(db.Integer)
    wis = db.Column(db.Integer)
    dex = db.Column(db.Integer)
    intel = db.Column(db.Integer)
    cha = db.Column(db.Integer)

    ancestry_feats = db.Column(db.Text)
    class_feats = db.Column(db.Text)

    spells = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship(User, backref="characters")


class Group(db.Model):
    """Group NPC(s) belong to"""

    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

    ##Why does this only work if 'character' and not 'characters'?
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    users = db.relationship(User, backref="groups")
    characters = db.relationship(Character, backref="groups")
