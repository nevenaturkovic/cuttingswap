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
from ..models import Conversation
from ..models import Message
from ..models import Offer
from ..models import OfferImage
from ..models import Permission
from ..models import Role
from ..models import User
from ..utils.image_upload import validate_image
from .forms import OfferForm
from ..messages.forms import StartConversationFormFromOffer


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
                file_ext = os.path.splitext(original_filename)[1].lower()
                if file_ext not in current_app.config[
                    "UPLOAD_EXTENSIONS"
                ] or file_ext != validate_image(image.stream):
                    flash(f'File "{original_filename}" is not a valid image.')
                    return render_template("offer/newoffer.html", form=form)
                offer_images.append((image, file_ext[1:]))
            else:
                flash("Invalid file uploaded.")
                return render_template("offer/newoffer.html", form=form)
        offer_images_db = []
        for image, ext in offer_images:
            offer_image = OfferImage(ext=ext)
            offer.images.append(offer_image)
            offer_images_db.append((image, offer_image))
        db.session.add(offer)
        db.session.commit()
        for image, row in offer_images_db:
            image.save(
                os.path.join(files_dir, f"{row.id}.{row.ext}")
            )

        return redirect(url_for(".offer", id=offer.id))
    return render_template("offer/newoffer.html", form=form)


@offer_bp.route("/images/<int:id>.<ext>")
def offer_image(id, ext):
    return send_from_directory(
        "../" + current_app.config["UPLOAD_PATH"] + "/offers", f"{id}.{ext}"
    )


@offer_bp.route("/<int:id>/thumbnail")
def thumbnail(id):
    offer = Offer.query.get_or_404(id)
    image = offer.images.order_by(OfferImage.id.asc()).first()
    if image:
        return redirect(url_for(".offer_image", id=image.id, ext=image.ext))
    return redirect(url_for("static", filename="no_image.svg"))


@offer_bp.route("/<int:id>", methods=["GET", "POST"])
@login_required
def offer(id):
    offer = Offer.query.get_or_404(id)
    form = StartConversationFormFromOffer()
    if form.validate_on_submit():
        participant_id = offer.author_id
        conversation = Conversation(
            initiator_id=current_user.id,
            participant_id=participant_id,
            offer_id=offer.id,
        )
        message = Message(
            sender_id=current_user.id,
            recipient_id=offer.author_id,
            body=form.message.data,
        )
        conversation.messages.append(message)
        db.session.add(conversation)
        db.session.commit()
        return redirect(
            url_for(
                "messages/single_conversation", id=conversation.id, form=form
            )
        )

    return render_template("offer/singleoffer.html", offer=offer, form=form)


@offer_bp.route("/")
@login_required
def list_of_offers():
    query = Offer.query

    try:
        location = request.args["location"]
        if location:
            query = query.filter(Offer.location.ilike(f"%{location}%"))
    except KeyError:
        pass

    try:
        title = request.args["title"]
        if title:
            query = query.filter(Offer.title.ilike(f"%{title}%"))
    except KeyError:
        pass

    own = False
    try:
        own = request.args["own"] == "yes"
    except KeyError:
        pass
    if not own:
        query = query.filter(Offer.author_id != current_user.id)

    page = request.args.get("page", 1, type=int)
    pagination = query.order_by(Offer.timestamp.desc()).paginate(
        page,
        per_page=current_app.config["CUTTINGSWAP_POSTS_PER_PAGE"],
        error_out=False,
    )
    offers = pagination.items
    return render_template(
        "offer/alloffers.html",
        offers=offers,
        pagination=pagination,
        oischema=OfferImage,
    )
