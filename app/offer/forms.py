from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import MultipleFileField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class OfferForm(FlaskForm):
    title = StringField("Title", validators=[Length(0, 64)])
    body = TextAreaField("What do you offer?", validators=[DataRequired()])
    location = StringField("Location", validators=[Length(0, 64)])
    images = MultipleFileField("Photo(s) Upload", validators=[DataRequired()])
    submit = SubmitField("Submit")
