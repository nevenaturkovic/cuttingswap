from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from . import offer as offer_bp
from .forms import OfferForm
from .. import db
from ..models import Permission, Role, User, Offer
from ..decorators import admin_required, permission_required

@offer_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_offer():
    form = OfferForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        offer = Offer(body=form.body.data,
                      author=current_user._get_current_object())
        db.session.add(offer)
        db.session.commit()
        return redirect(url_for('.offer'))
    offers = Offer.query.order_by(Offer.timestamp.desc()).all()
    return render_template('offer/newoffer.html', form=form)