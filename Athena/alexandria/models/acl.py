from database import db
from datetime import datetime,timedelta

class ACLState():
    REQUESTED = 1
    GRANTED = 2
    REVOKED = 3
    
class ACL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    access_level = db.Column(db.String(10), nullable=False)
    borrowed_on = db.Column(db.DateTime, default=datetime.now)
    due_on = db.Column(db.DateTime, nullable=True)
    returned_on = db.Column(db.DateTime, nullable=True)

    user = db.relationship('Users', backref='access_levels')
    book = db.relationship('Books', backref='access_levels')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'access_level': self.access_level,
            'borrowed_on': self.borrowed_on.isoformat(),
            'due_on': self.due_on.isoformat() if self.due_on else None,
            'returned_on': self.due_on.isoformat() if self.returned_on else None,
        }

    def approve_request(self):
        self.borrowed_on = datetime.now()
        self.due_on = datetime.now() + timedelta(days=7)
        self.access_level = ACLState.GRANTED
        
    def revoke_request(self):
        self.returned_on = datetime.now()
        self.access_level = ACLState.REVOKED

    def get_user_id(self):
        return self.user_id

    def get_book_id(self):
        return self.book_id
    
    def get_access_level(self):
        return self.access_level