from flask import abort
from flask import current_app
from flask import flash
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from . import main
from .. import db
from ..decorators import admin_required
from ..decorators import permission_required


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/home")
def home():
    return render_template("home.html")
