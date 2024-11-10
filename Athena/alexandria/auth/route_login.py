from flask import request, jsonify
from flask_jwt_extended import create_access_token

from auth import auth_bp
from models.user import Users

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity={'userID': user.id, 'username': user.username, 'isLibrarian': bool(user.isLibrarian)})
    return jsonify(access_token=access_token,isLibrarian=user.isLibrarian), 200
