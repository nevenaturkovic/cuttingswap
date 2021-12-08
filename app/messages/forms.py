from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import MultipleFileField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Regexp

from ..models import Offer
from ..models import Role
from ..models import User


class StartConversationForm(FlaskForm):
    subject = StringField("Subject", validators=[Length(0, 64)])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")


class StartConversationFormFromOffer(FlaskForm):
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")


class MessageForm(FlaskForm):
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")
