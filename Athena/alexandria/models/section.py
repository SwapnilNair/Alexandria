from database import db
from datetime import datetime

class Sections(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    books = db.relationship('Books', backref='sections', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
        }