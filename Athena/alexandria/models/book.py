from database import db
from datetime import datetime

class Books(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_url':self.image_url,
            'description': self.description,
            'contents':self.contents,
            'created_at': self.created_at.isoformat(),
            'section_id': self.section_id,
        }
    
    def safe_to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_url':self.image_url,
            'description': self.description,
            'contents':"",
            'created_at': self.created_at.isoformat(),
            'section_id': self.section_id,
        }