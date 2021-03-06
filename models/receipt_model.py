from datetime import datetime
from db import db


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(80), unique=True, nullable=False)
    provider_id = db.Column(db.Integer, default=0)
    amount = db.Column(db.Integer, default=0)
    received = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().date)
    added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().date)
    url = db.Column(db.String(80), unique=False)
    info = db.Column(db.Text, unique=False)

    def __repr__(self):
        return f"<Receipt {self.provider_id} - {self.number}>"
