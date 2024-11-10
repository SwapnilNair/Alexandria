
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from auth import auth_bp
from database import db

from models.user import Users

@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    current_user = get_jwt_identity()
    if not current_user['isLibrarian']:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    isLibrarian = data.get('isLibrarian', False)

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if Users.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = Users(username=username, isLibrarian=isLibrarian)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"debug": "User created successfully"}), 201
