from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.acl import ACL,ACLState
from models.book import Books
from models.user import Users
from datetime import datetime,timedelta
from routes.check_role import librarian_only

acl_bp = Blueprint('acl', __name__)

@acl_bp.route('/books', methods=['GET'])
@jwt_required()
def get_user_books():
    user_id = get_jwt_identity()
    print(ACLState.REQUESTED)

    access_levels = [ACLState.REQUESTED,ACLState.GRANTED,ACLState.REVOKED]
    acl_entries = ACL.query.filter_by(user_id=user_id).filter(ACL.access_level.in_(access_levels)).all()
    
    books = []
    for entry in acl_entries:
        book = Books.query.get(entry.book_id)
        if book:
            books.append({
                'book': book.to_dict(),
                'access_level': entry.access_level
            })
    
    return jsonify(books)

@acl_bp.route('/requestBook', methods=['POST'])
@jwt_required()
def add_acl_entry():
    data = request.get_json()
    user = get_jwt_identity()
    if user['isLibrarian']:
        return jsonify({"msg":"you are the librarian"}), 400
    
    user_id = user.get('userID')
    book_id = data.get('book_id')

    access_level = ACLState.REQUESTED
    borrowed_on = data.get('borrowed_on', datetime.now())
    due_on = data.get('due_on', datetime.now()+ timedelta(days=7) )

    if not user_id or not book_id or not access_level:
        return jsonify({"msg": "User ID, Book ID, and Access Level are required"}), 400

    if access_level != ACLState.REQUESTED:
        return jsonify({"msg": "Invalid Access Level"}), 400
    print("USER ID : ",user_id,"BOOK ID : ",book_id)

    if ACL.query.filter_by(user_id = user_id,book_id = book_id,access_level = access_level).count() :
        return jsonify({"msg": "You have already made a request for this book"}), 400

    new_acl = ACL(
        user_id=user_id,
        book_id=book_id,
        access_level=access_level,
        borrowed_on=borrowed_on,
        due_on=due_on
    )
    
    db.session.add(new_acl)
    db.session.commit()

    return jsonify({"msg":"requested successfully"}), 201

@acl_bp.route('/approveRequest', methods=['POST'])
@jwt_required()
@librarian_only
def approve_request():
    data = request.get_json()
    request_id = data.get('request_id')

    book_request = ACL.query.get(request_id)
    print(book_request)
    if book_request == None:
        return jsonify({"error":"request doesn't exist"}), 400
    if int(book_request.access_level) != int(ACLState.REQUESTED):
        return jsonify({"error":"request already approved"}), 400

    book_request.approve_request()
    db.session.commit()

    return jsonify({"msg":"request approved successfully"}), 201

@acl_bp.route('/revokeRequest', methods=['POST'])
@jwt_required()
@librarian_only
def revoke_request():
    data = request.get_json()
    request_id = data.get('request_id')

    book_request = ACL.query.get(request_id)
    print(book_request)
    if book_request == None:
        return jsonify({"error":"issue doesn't exist"}), 400
    if int(book_request.access_level) != int(ACLState.GRANTED):
        return jsonify({"error":"book no "}), 400

    book_request.revoke_request()
    db.session.commit()

    return jsonify({"msg":"request approved successfully"}), 201


@acl_bp.route('/all', methods=['POST'])
@jwt_required()
@librarian_only
def get_acl_entries():
    acl_entries = ACL.query \
        .filter_by(access_level=ACLState.REQUESTED) \
        .join(Books, ACL.book_id == Books.id) \
        .join(Users, ACL.user_id == Users.id) \
        .all()
    
    response = []
    for entry in acl_entries:
        entry_dict = entry.to_dict()
        entry_dict['book_name'] = entry.book.name  
        entry_dict['user_name'] = entry.user.username  
        response.append(entry_dict)

    return jsonify(response)

@acl_bp.route('/allissued', methods=['POST'])
@jwt_required()
@librarian_only
def get_issued():
    acl_entries = ACL.query \
        .filter_by(access_level=ACLState.GRANTED) \
        .join(Books, ACL.book_id == Books.id) \
        .join(Users, ACL.user_id == Users.id) \
        .all()
    
    response = []
    for entry in acl_entries:
        entry_dict = entry.to_dict()
        entry_dict['book_name'] = entry.book.name  
        entry_dict['user_name'] = entry.user.username  
        response.append(entry_dict)

    return jsonify(response)

@acl_bp.route('/books/return', methods=['POST'])
@jwt_required()
def return_book():
    data = request.get_json()
    user = get_jwt_identity()
    
    if user['isLibrarian']:
        return jsonify({"msg": "Librarians cannot return books"}), 400
    
    user_id = user.get('userID')
    book_id = data.get('book_id')

    if not user_id or not book_id:
        return jsonify({"msg": "User ID and Book ID are required"}), 400
    

    acl_entry = ACL.query.filter_by(user_id=user_id, book_id=book_id, access_level=ACLState.GRANTED).first()

    if not acl_entry:
        return jsonify({"msg": "No request found for this book by this user"}), 404


    if int(acl_entry.access_level) != int(ACLState.GRANTED):
        return jsonify({"msg": "This book is not currently requested by you"}), 400

    acl_entry.revoke_request()
    db.session.commit()

    return jsonify({"msg": "Book marked as returned successfully"}), 200

@acl_bp.route('/allusers', methods=['POST'])
@jwt_required()
@librarian_only
def get_users():
    users = Users.query.all()
    return jsonify({"users" :len(users)}),200