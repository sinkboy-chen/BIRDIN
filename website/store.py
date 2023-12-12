from flask import Blueprint, flash, request, redirect, url_for
from flask_login import login_required, current_user
from urllib.parse import unquote

from .models import UserSpecies, Species, NicknameHistory
from . import db

store = Blueprint("store", __name__)

@store.route("/buy_collection", methods=["POST"])
@login_required
def buy_collection():
    species = request.form.get("species")
    species = unquote(species)
    species = Species.query.filter_by(name=species).first()
    relationship = UserSpecies.query.filter_by(user_id=current_user.id, species_id=species.id).first()

    if not species:
        flash("is it alien? no one found yet")
    elif not species.collection_status:
        flash("currently don't have collection")
    elif not relationship:
        flash("sound not collected yet") 
    elif relationship.relationship_type==1:
        flash("already bought")
    elif current_user.tokens<20:
        flash("token not enough")
    else:
        current_user.tokens -= 20
        relationship.relationship_type=1
        db.session.commit()
        flash("successfully bought")
    return redirect(url_for("views.species_detail", name=species.name))

@store.route("/assign_nickname", methods=["POST"])
@login_required
def assign_nickname():
    species = request.form.get("species")
    species = unquote(species)
    nickname = request.form.get("nickname")
    species = Species.query.filter_by(name=species).first()
    relationship = UserSpecies.query.filter_by(user_id=current_user.id, species_id=species.id).first()

    if not species:
        flash("is it alien? no one found yet")
    elif not relationship:
        flash("sound not collected yet") 
    elif current_user.tokens<(species.change_nickname_cycle + 10):
        flash("token not enough")
    elif len(nickname)>30:
        flash("nickname too long^_^")
    else:
        current_user.tokens -= (species.change_nickname_cycle + 10)
        species.nickname = nickname
        species.change_nickname_cycle += 1
        species.named_by = current_user
        new_nickname_history = NicknameHistory(
            user_id = current_user.id,
            species_id = species.id,
            nickname = nickname,
            cost = (species.change_nickname_cycle + 10)
        )
        db.session.add(new_nickname_history)
        db.session.commit()
        flash("successfully assigned")
    return redirect(url_for("views.species_detail", name=species.name))




