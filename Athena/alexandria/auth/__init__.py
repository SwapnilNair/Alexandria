from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


from . import route_login,route_register,route_test






