import os

from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from werkzeug.utils import secure_filename

from . import offer as offer_bp
from .. import db
from ..decorators import admin_required
from ..decorators import permission_required
from ..models import Offer
from ..models import OfferImage
from ..models import Permission
from ..models import Role
from ..models import User
from ..utils.image_upload import validate_image
from .forms import OfferForm


@offer_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_offer():
    form = OfferForm()
    files_dir = current_app.config["UPLOAD_PATH"] + "/offers"
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        offer = Offer(
            title=form.title.data,
            body=form.body.data,
            location=form.location.data,
            author=current_user._get_current_object(),
        )
        offer_images = []
        for image in form.images.data:
            original_filename = secure_filename(image.filename)
            if original_filename != "":
                file_ext = os.path.splitext(original_filename)[1]
                if file_ext not in current_app.config[
                    "UPLOAD_EXTENSIONS"
                ] or file_ext != validate_image(image.stream):
                    flash(f'File "{original_filename}" is not a valid image.')
                    return render_template("offer/newoffer.html", form=form)
                offer_image = OfferImage(ext=file_ext[1:])
                db.session.add(offer_image)
                db.session.commit()
                offer_images.append(offer_image)
                image.save(
                    os.path.join(
                        files_dir, f"{offer_image.id}.{offer_image.ext}"
                    )
                )
            else:
                flash("Invalid file uploaded.")
                return render_template("offer/newoffer.html", form=form)
        db.session.add(offer)
        db.session.commit()
        for offer_image in offer_images:
            offer_image.offer_id = offer.id
        db.session.commit()
        return redirect(url_for(".offer", id=offer.id))
    return render_template("offer/newoffer.html", form=form)


@offer_bp.route("/images/<int:id>.<ext>")
def offer_image(id, ext):
    return send_from_directory(
        "../" + current_app.config["UPLOAD_PATH"] + "/offers", f"{id}.{ext}"
    )


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
