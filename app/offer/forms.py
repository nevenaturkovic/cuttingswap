from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User, Offer

class OfferForm(FlaskForm):
    title = StringField('Title', validators=[Length(0, 64)])
    body = TextAreaField("What do you offer?", validators=[DataRequired()])
    location = StringField('Location', validators=[Length(0, 64)])
    submit = SubmitField('Submit')
