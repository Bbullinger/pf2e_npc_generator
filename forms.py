from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
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

    name = StringField("Name", validators=[InputRequired()])
    background = StringField("Background", validators=[InputRequired()])
    ancestry = StringField("Ancestry", validators=[InputRequired()])
    char_class = StringField("Class", validators=[InputRequired()])

    level = IntegerField("Level")

    strength = IntegerField("Str")
    con = IntegerField("Con")
    wis = IntegerField("Wis")
    dex = IntegerField("Dex")
    intel = IntegerField("Int")
    cha = IntegerField("Cha")
    save_button1 = SubmitField("Save")

    # ancestry_feats = StringField("Ancestry Feats")
    # class_feats = StringField("Class Feats")

    # spells = StringField("Spells")


#####Will need to revist how user adds character to a specific group. Should it be a form?


class GroupForm(FlaskForm):
    """Create a Group for NPCs to join"""

    group_name = StringField("Group Name", validators=[InputRequired()])
    save_button2 = SubmitField("New")


class JoinGroup(FlaskForm):

    group_name = StringField("Group Name", validators=[InputRequired()])
    npc_to_join = StringField("Character Name", validators=[InputRequired()])
