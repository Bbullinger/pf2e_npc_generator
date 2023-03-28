from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email


class UserAddForm(FlaskForm):
    """Form for adding users, email used for password reseting"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("E-mail", validators=[InputRequired(), Email()])


class LoginForm(FlaskForm):
    """Log in a previously created user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class NpcGenerator(FlaskForm):
    """Form for generating the random character"""

    name = StringField("Name")
    background = StringField("Background")
    ancestry = StringField("Ancestry")
    char_class = StringField("Class")

    level = IntegerField("Level")

    strength = IntegerField("Str")
    con = IntegerField("Con")
    wis = IntegerField("Wis")
    dex = IntegerField("Dex")
    intel = IntegerField("Int")
    cha = IntegerField("Cha")

    ancestry_feats = StringField("Ancestry Feats")
    class_feats = StringField("Class Feats")

    spells = StringField("Spells")


#####Will need to revist how user adds character to a specific group. Should it be a form?


class Group(FlaskForm):
    """Create a Group for NPCs to join"""

    group_name = StringField("Group Name", validators=[InputRequired()])


class JoinGroup(FlaskForm):

    group_name = StringField("Group Name", validators=[InputRequired()])
    npc_to_join = StringField("Character Name", validators=[InputRequired()])
