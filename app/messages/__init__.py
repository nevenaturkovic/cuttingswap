from flask import Blueprint

messages = Blueprint("messages", __name__)

from . import views
from ..models import Permission


@messages.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
