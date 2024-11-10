from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS


from auth import auth_bp 
from routes.route_book import books_bp
from routes.route_section import sections_bp
from routes.route_acl import acl_bp

from auth.seed import seedLibrarian
from database import db
from .config import app

def New():
    app.logger.setLevel("DEBUG")
    log = app.logger
    log.info("Logger initialized")

    db.init_app(app)
    app.app_context().push()
    db.create_all()
    log.info("Database initialized")

    err = seedLibrarian()
    if err != None:
        log.error(err)
    log.info("Database seeded with admin")

    CORS(app, resources={r'/*': {'origins': '*'}})

    jwtService = JWTManager(app)

    log.info("Cache initialized")

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(sections_bp, url_prefix='/api/sections')
    app.register_blueprint(acl_bp,url_prefix="/api/acl")
    log.info("API service initialized")


    @app.route("/ping")
    def index():
        return "hey swapnil"

    return app




