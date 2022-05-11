from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class add_song_form(FlaskForm):
    title = TextAreaField('Title', [
        validators.DataRequired(),
        validators.length(max=300)
    ], description="Song title")

    artist = TextAreaField('Artist', [
        validators.DataRequired(),
        validators.length(max=300)
    ], description="Song artist")

    genre = TextAreaField('Genre', [
        validators.DataRequired(),
        validators.length(max=300)
    ], description="Song genre")

    year = IntegerField('Year', [
        validators.DataRequired(),
    ], description="Song release year")

    submit = SubmitField()


class song_edit_form(FlaskForm):
    title = TextAreaField('Title', [
        validators.DataRequired(),
        validators.length(max=300)
    ], description="Song title")

    artist = TextAreaField('Artist', [
        validators.DataRequired(),
        validators.length(max=300)
    ], description="Song artist")

    genre = TextAreaField('Genre', [
        validators.DataRequired(),
        validators.length(max=300)
    ], description="Song genre")

    year = IntegerField('Year', [
        validators.DataRequired(),
    ], description="Song release year")

    submit = SubmitField()