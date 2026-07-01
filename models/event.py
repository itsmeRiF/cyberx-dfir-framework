from database.db import db
from datetime import datetime

class Event(db.Model):

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    case_id = db.Column(db.Integer, db.ForeignKey("cases.id"))

    event_id = db.Column(db.String(50))
    provider = db.Column(db.String(255))
    level = db.Column(db.String(50))
    message = db.Column(db.Text)

    timestamp = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)