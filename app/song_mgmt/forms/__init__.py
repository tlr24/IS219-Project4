from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class add_song_form(FlaskForm):
    title = TextAreaField('Title', [
        validators.DataRequired(),
    ], description="Song title")

    artist = TextAreaField('Artist', [
        validators.DataRequired(),
    ], description="Song artist")

    genre = TextAreaField('Genre', [
        validators.DataRequired(),
    ], description="Song genre")

    year = IntegerField('Year', [
        validators.DataRequired(),
    ], description="Song release year")

    submit = SubmitField()