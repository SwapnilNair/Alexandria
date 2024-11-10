from flask_jwt_extended import  get_jwt_identity
from functools import wraps
from flask import jsonify

def librarian_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity.get('isLibrarian'):
            return fn(*args, **kwargs)
        else:
            return jsonify({"msg": "Librarian access required"}), 403
    return wrapper