from flask import Blueprint, jsonify,request
from database import db
from models.section import Sections
from models.book import Books
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.check_role import librarian_only

sections_bp = Blueprint('sections', __name__)

@sections_bp.route('/list', methods=['POST'])
@jwt_required()
def get_all_sections():
    sections = Sections.query.all()
    return jsonify([section.to_dict() for section in sections])

@sections_bp.route('/list/<int:section_id>/books', methods=['POST'])
@jwt_required()
def get_books_by_section(section_id):
    section = Sections.query.get(section_id)
    return jsonify([book.to_dict() for book in section.books])

@sections_bp.route('/list/<int:section_id>', methods=['POST'])
@jwt_required()
def get_section_by_id(section_id):
    section = Sections.query.get(section_id)
    return jsonify(section.to_dict())

@sections_bp.route('/add', methods=['POST'])
@jwt_required()
@librarian_only
def add_section():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    new_section = Sections(
        name=name, 
        description=description)
    
    if Sections.query.filter_by(name=name).first():
        return jsonify({"error": "Section already exists"}), 400
    
    db.session.add(new_section)
    db.session.commit()

    return jsonify({"msg": "success : add section"}), 201

@sections_bp.route('/update/<int:id>', methods=['POST'])
@jwt_required()
@librarian_only
def update_section(id):
    data = request.get_json()

    if not id:
        return jsonify({"error": "ID is required"}), 400

    book = Sections.query.get(id)

    if not book:
        return jsonify({"error": "Section not found"}), 404

    if 'name' in data:
        book.name = data['name']
    if 'description' in data:
        book.description = data['description']

    
    db.session.commit()

    return jsonify({"msg": "Success: Section updated"}), 200

@sections_bp.route('/del/<int:id>', methods=['POST'])
@jwt_required()
@librarian_only
def del_section(id):
    if not id :
        return jsonify({"error": "ID is required"}), 400

    section = Sections.query.get(id)

    if not section:
        return jsonify({"error": "section not found"}), 404
    
    Books.query.filter_by(section_id=id).delete()

    db.session.delete(section)
    db.session.commit()
    return jsonify({"msg": "success : del section"}), 204

