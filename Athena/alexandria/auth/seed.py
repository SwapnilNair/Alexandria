from database import db
from models.user import Users

def seedLibrarian():
    username = "admin"
    password = "admin123"
    isLibrarian = True
    if Users.query.filter_by(username=username).first():
        return None
    try:
        new_user = Users(username=username, isLibrarian=isLibrarian)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return str(e)
    
    return None