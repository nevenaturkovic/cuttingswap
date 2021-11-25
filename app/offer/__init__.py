from flask import Blueprint

offer = Blueprint("offer", __name__)

from . import views
from ..models import Permission


@offer.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
