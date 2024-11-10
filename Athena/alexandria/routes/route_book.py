from flask import Blueprint, jsonify,request
from database import db
from models.book import Books
from models.section import Sections
from models.acl import ACL,ACLState

from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.check_role import librarian_only
from application.config import cache

books_bp = Blueprint('books', __name__)

@books_bp.route('/list', methods=['POST'])
@jwt_required()
@cache.cached(timeout=10)
def get_all_books():
    books = Books.query.all()
    return jsonify([book.safe_to_dict() for book in books])

@books_bp.route('/add', methods=['POST'])
@jwt_required()
@librarian_only
def add_book():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    contents = data.get('contents')
    sectionID = data.get('sectionID')
    imageURL = data.get('image_url')

    if not name :
        return jsonify({"error": "Name is required"}), 400
    
    if not contents:
        return jsonify({"error": "Contents are required"}), 400
    
    if not sectionID:
        return jsonify({"error": "Section is required"}), 400

    if Books.query.filter_by(name=name).first() != None:
        return jsonify({"error": "Book already exists"}), 400

    if Sections.query.get(sectionID) == None:
        return jsonify({"error": "Section doesn't exist"}), 400

    new_book = Books(
        name=name, 
        description=description,
        contents = contents,
        section_id = sectionID, image_url = imageURL)
    
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"msg": "success : add book"}), 201

@books_bp.route('/list/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book_by_id(book_id):
    book = Books.query.get(book_id)
    return jsonify(book.to_dict())

@books_bp.route('/list/mybooks',methods=['POST'])
@jwt_required()
def get_my_books():
    userID = get_jwt_identity()['userID']

    my_books = ACL.query.filter_by(user_id = userID,access_level = ACLState.GRANTED).all()
    
    book_list = []
    for entry in my_books:
        book = Books.query.get(entry.book_id)
        if book:
           
            book_data = book.safe_to_dict()  
            book_data['due_on'] = entry.due_on if entry.due_on else None
            book_list.append(book_data)

    return book_list

@books_bp.route('/list/myreqs',methods=['POST'])
@jwt_required()
def get_my_books_requested():
    userID = get_jwt_identity()['userID']

    my_books = ACL.query.filter_by(user_id = userID,access_level = ACLState.REQUESTED).all()
    
    book_list = []
    for entry in my_books:
        book = Books.query.get(entry.book_id)
        if book:
            book_data = book.safe_to_dict()  
            book_data['borrowed_on'] = entry.borrowed_on if entry.borrowed_on else None
            book_list.append(book_data)
    
    return jsonify(book_list)

@books_bp.route('/list/myrevoked',methods=['POST'])
@jwt_required()
def get_my_books_revoked():
    userID = get_jwt_identity()['userID']

    my_books = ACL.query.filter_by(user_id = userID,access_level = ACLState.REVOKED).all()
    
    book_list = []
    for entry in my_books:
        book = Books.query.get(entry.book_id)
        if book:
            book_list.append(book)
    
    return jsonify([entry.safe_to_dict() for entry in book_list])

@books_bp.route('/del/<int:id>', methods=['POST'])
@jwt_required()
@librarian_only
def del_book(id):
    if not id :
        return jsonify({"error": "ID is required"}), 400

    book = Books.query.get(id)

    if not book:
        return jsonify({"error": "book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()

    return jsonify({"msg": "success : del book"}), 201

@books_bp.route('/update/<int:id>', methods=['POST'])
@jwt_required()
@librarian_only
def update_book(id):
    data = request.get_json()

    if not id:
        return jsonify({"error": "ID is required"}), 400

    book = Books.query.get(id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    if 'name' in data:
        book.name = data['name']
    if 'description' in data:
        book.description = data['description']
    if 'image_url' in data:
        book.image_url = data['image_url']

    
    db.session.commit()

    return jsonify({"msg": "Success: Book updated"}), 200
