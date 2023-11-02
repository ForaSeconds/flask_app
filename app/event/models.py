from app.database import db
from sqlalchemy import ForeignKey
from datetime import datetime


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[created_by])
    begin_at = db.Column(db.Date, nullable=False, default=datetime.now)
    end_at = db.Column(db.Date, nullable=False, default=datetime.now)
    max_users = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=True)


class EventUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer, nullable=True)
    event = db.relationship('User', foreign_keys=[event_id])
    user = db.relationship('Event', foreign_keys=[user_id])
