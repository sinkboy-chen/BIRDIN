from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid

class UserSpecies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    # 0 for gathered
    # 1 for loved
    relationship_type = db.Column(db.Boolean)
    last_gathered_date = db.Column(db.Date)
    species = db.relationship("Species")
    
class UnverifiedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    username = db.Column(db.String)
    show_student_id = db.Column(db.Boolean)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=str(uuid.uuid4()))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    username = db.Column(db.String)
    show_student_id = db.Column(db.Boolean)

    tokens = db.Column(db.Integer)
    all_owned_species = db.relationship('UserSpecies')
    nickname_history_entries = db.relationship('NicknameHistory', backref='user', lazy='dynamic')
    def get_naming_history(self):
        return self.nickname_history_entries.order_by(NicknameHistory.timestamp.desc()).all()

class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    change_nickname_cycle = db.Column(db.Integer)
    nickname = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    named_by = db.relationship("User")
    nickname_histories = db.relationship('NicknameHistory', backref='species',lazy='dynamic')
    def get_nickname_history(self):
        return self.nickname_histories.order_by(NicknameHistory.timestamp.desc()).all()
    collection_status = db.Column(db.Boolean)

class NicknameHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    nickname = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # UTC time by default
    cost = db.Column(db.Integer)