from flask import Flask
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_pyfile("../config.py")

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10, encoding='utf-8')

file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))

file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)

from . import views

from .users import views
app.register_blueprint(views.users_bp)

from .products import products_bp
app.register_blueprint(products_bp, url_prefix="/shop")