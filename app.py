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
from forms import UserAddForm, LoginForm, NpcGenerator, GroupForm, JoinGroup


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
def main_page():
    """Present character form to user"""
    npc_form = NpcGenerator()
    group_form = GroupForm()

    if npc_form.save_button1.data and npc_form.validate_on_submit():
        character = Character(
            name=npc_form.name.data,
            background=npc_form.background.data,
            ancestry=npc_form.ancestry.data,
            char_class=npc_form.char_class.data,
            level=npc_form.level.data,
            strength=npc_form.strength.data,
            con=npc_form.con.data,
            wis=npc_form.wis.data,
            dex=npc_form.dex.data,
            intel=npc_form.intel.data,
            cha=npc_form.cha.data,
            # ancestry_feats=form.ancestry_feats.data,
            # class_feats=form.class_feats.data,
            # spells=form.spells.data,
            user_id=g.user.id,
        )
        db.session.add(character)
        db.session.commit()
        flash("Character added to roster.")
        return redirect("/")

    if group_form.save_button2.data and group_form.validate_on_submit():
        group = Group(group_name=group_form.group_name.data, user_id=g.user.id)

        db.session.add(group)
        db.session.commit()
        flash("Group added to list.")
        return redirect("/")

    return render_template("index.html", npc_form=npc_form, group_form=group_form)


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


######Retrieve info from the API and Database###########
@app.route("/<endpoint>")
def randomAPI(endpoint):
    response = requests.get(BASE_URL + endpoint, headers={"Authorization": API_KEY})
    return response.text


@app.route("/get_characters")
def getDatabaseCharacters():
    if not g.user:
        flash("Please log in")
        return redirect("/")
    characters = Character.query.filter(Character.user_id == g.user.id).all()
    serialized_characters = []
    for character in characters:
        serialized_characters.append(character.serialize_character())
    return serialized_characters


@app.route("/get_groups")
def getDatabaseGroups():
    if not g.user:
        flash("Please log in")
        return redirect("/")
    groups = Group.query.filter(Group.user_id == g.user.id).all()
    serialized_groups = []
    for group in groups:
        serialized_groups.append(group.serialize_group())
    print("test")
    return serialized_groups
