import os
from flask import Flask
from flask_caching import Cache

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    Debug = True
    SECRET_KEY = "U3dhcG5pbCBOYWly"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "../database",'alexandria.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "U3dhcG5pbCBOYWlyw"
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_KEY_PREFIX = "alex"
    CACHE_DEFAULT_TIMEOUT = 10


app = Flask(__name__)
app.config.from_object(Config)
cache = Cache(app)
