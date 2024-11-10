from flask import  jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from auth import auth_bp

@auth_bp.route('/tester', methods=['GET'])
@jwt_required()
def tester():
    current_user = get_jwt_identity()
    if current_user['isLibrarian']:
        return jsonify(message="Hello Librarian"), 200
    else:
        return jsonify(message="Hello User"), 200