from flask import Blueprint, request, current_app

from . import db
from .models import UserSpecies, UnverifiedUser, User, Species, NicknameHistory

admin = Blueprint("admin", __name__)

@admin.route("/initialize_db", methods=["POST"])
def initialize_db():
    if request.form.get("key")==current_app.config["ADMIN_KEY"]:
        db.session.query(NicknameHistory).delete()
        db.session.query(UserSpecies).delete()
        db.session.query(Species).delete()
        db.session.query(User).delete()
        db.session.query(UnverifiedUser).delete()
        
        
        
        db.session.commit()
        return "successfully initialized database", 200
    else:
        return "invalid key", 200


    



