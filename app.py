import os
from random import randint
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.pathfinder2.fr/v1/pf2/"
CURR_USER_KEY = "curr_user"

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from sqlalchemy.exc import IntegrityError

from models import User, Character, Group, db, app
from forms import UserAddForm, LoginForm, NpcGenerator, Group, JoinGroup


@app.before_request
def add_user_to_g():
    """Check if user is logged in, if so add to g global variable"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def login(user):
    session[CURR_USER_KEY] = user.id


def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/", methods=["GET", "POST"])
def home_page():
    """Present character form to user"""
    form = NpcGenerator()

    if form.validate_on_submit():
        character = Character(
            name=form.name.data,
            background=form.background.data,
            ancestry=form.ancestry.data,
            char_class=form.char_class.data,
            level=form.level.data,
            strength=form.strength.data,
            con=form.con.data,
            wis=form.wis.data,
            dex=form.dex.data,
            intel=form.intel.data,
            cha=form.cha.data,
            ancestry_feats=form.ancestry_feats.data,
            class_feats=form.class_feats.data,
            spells=form.spells.data,
            user_id=g.user.id,
        )
        print("***************************WORKING**********************")
        db.session.add(character)
        db.session.commit()
        flash("Character added to roster.")
        return redirect("/")
    return render_template("index.html", form=form)


@app.route("/add_character")

################USER LOG IN/SIGN UP ROUTES############################
@app.route("/signup", methods=["GET", "POST"])
def user_signup():
    """Allow user to sign up, create new user and add to database.
    if username already exists, flash error message."""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()
            login(user)
            return redirect("/")
        except IntegrityError:
            flash("Username already taken.", "danger")
            return redirect("/signup")

    else:
        return render_template("signup.html", form=form)


@app.route("/logout")
def user_logout():
    if session[CURR_USER_KEY]:
        flash(f"{g.user.username} logged out.")
        logout()
        return redirect("/")
    else:
        flash("You are not logged in.")
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def user_sign_in():
    """When user signs up, stored password is hashed. When validating credentials entered password
    is hashed, then checked against stored hashed password."""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login(user)
            flash(f"{user.username} successfully logged in.")
            return redirect("/")
        else:
            flash("Invalid credentials.", "danger")
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


######Retrieve info from the API###########
@app.route("/<endpoint>")
def randomAPI(endpoint):
    response = requests.get(BASE_URL + endpoint, headers={"Authorization": API_KEY})
    return response.text
