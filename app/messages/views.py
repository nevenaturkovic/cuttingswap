from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import current_app
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from . import messages as messages_bp
from .. import db
from ..models import Message
from ..models import Offer
from ..models import Conversation
from ..models import User
from .forms import StartConversationForm
from .forms import StartConversationFormFromOffer
from .forms import MessageForm


@messages_bp.route("/")
@login_required
def all_conversations():
    query = Conversation.query.filter(
        Conversation.initiator_id == current_user.id
        or Conversation.participant_id == current_user.id
    )
    page = request.args.get("page", 1, type=int)
    pagination = query.paginate(
        page,
        per_page=current_app.config["CUTTINGSWAP_POSTS_PER_PAGE"],
        error_out=False,
    )
    conversations = pagination.items
    return render_template(
        "messages/all_conversations.html",
        conversations=conversations,
        pagination=pagination,
    )


@messages_bp.route("/<int:id>", methods=["GET", "POST"])
@login_required
def single_conversation(id):
    conversation = Conversation.query.get_or_404(id)
    if not (
        conversation.initiator_id == current_user.id
        or conversation.participant_id == current_user.id
    ):
        abort(404)
    form = MessageForm()
    if form.validate_on_submit():
        recipient_id = (
            conversation.initiator_id
            if conversation.initiator_id != current_user.id
            else conversation.participant_id
        )
        message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            body=form.message.data,
            conversation_id=id,
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for(".single_conversation", id=id))

    return render_template(
        "messages/conversation.html",
        form=form,
        conversation=conversation,
    )


@messages_bp.route("/new_conversation", methods=["GET", "POST"])
@login_required
def new_conversation():
    if list(request.args.keys()) == ["user"]:
        username = request.args["user"]
        return _new_conversation_for_user(username)
    if list(request.args.keys()) == ["offer"]:
        offer_id = request.args["offer"]
        return _new_conversation_regarding_offer(offer_id)
    abort(404)


def _new_conversation_for_user(username):
    initiator_id = current_user.id
    participant = User.query.filter_by(username=username).first()
    if not participant or participant.id == initiator_id:
        abort(404)

    form = StartConversationForm()
    if form.validate_on_submit():
        participant_id = participant.id
        conversation = Conversation(
            initiator_id=initiator_id,
            participant_id=participant_id,
            subject=form.subject.data,
        )
        message = Message(
            sender_id=initiator_id,
            recipient_id=participant_id,
            body=form.message.data,
        )
        conversation.messages.append(message)
        db.session.add(conversation)
        db.session.commit()

        return redirect(url_for(".single_conversation", id=conversation.id))

    return render_template(
        "messages/new_conversation.html",
        form=form,
        username=username,
        show_subject=True,
    )


def _new_conversation_regarding_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    initiator_id = current_user.id
    if initiator_id == offer.author_id:
        abort(404)
    existing_conversation = Conversation.query.filter_by(
        initiator_id=initiator_id, offer_id=offer_id
    ).first()
    if existing_conversation:
        return redirect(
            url_for(".single_conversation", id=existing_conversation.id)
        )

    form = StartConversationFormFromOffer()
    if form.validate_on_submit():
        participant_id = offer.author_id
        conversation = Conversation(
            initiator_id=initiator_id,
            participant_id=participant_id,
            offer_id=offer_id,
        )
        message = Message(
            sender_id=initiator_id,
            recipient_id=participant_id,
            body=form.message.data,
        )
        conversation.messages.append(message)
        db.session.add(conversation)
        db.session.commit()
        return redirect(url_for(".single_conversation", id=conversation.id))

    return render_template(
        "messages/new_conversation.html",
        form=form,
        offer=offer,
        show_subject=False,
    )
