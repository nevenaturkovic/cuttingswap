from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from . import offer as offer_bp
from .. import db
from ..decorators import admin_required
from ..decorators import permission_required
from ..models import Offer
from ..models import Permission
from ..models import Role
from ..models import User
from .forms import OfferForm


@offer_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_offer():
    form = OfferForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        offer = Offer(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
        db.session.add(offer)
        db.session.commit()
        return redirect(url_for(".offer", id=offer.id))
    return render_template("offer/newoffer.html", form=form)


@offer_bp.route("/<int:id>")
@login_required
def offer(id):
    offer = Offer.query.get_or_404(id)
    return render_template("offer/singleoffer.html", offer=offer)

@offer_bp.route("/")
@login_required
def list_of_offers():
    offers = Offer.query.order_by(Offer.timestamp.desc()).all()
    return render_template("offer/alloffers.html", offer=offer, offers=offers)
