from flask import Flask
import os
import logging
from logging.handlers import RotatingFileHandler

# --- 1. Application Initialization ---
app = Flask(__name__)

# --- 2. Configuration Loading ---
"""Load configuration settings from a file located one directory up."""
app.config.from_pyfile("../config.py")

# --- 3. Logging Configuration ---
# Ensure the 'logs' directory exists before trying to write to it.
if not os.path.exists('logs'):
    os.mkdir('logs')
"""
Set up a rotating file handler for logging.
This prevents log files from becoming excessively large.
- 'logs/app.log': The file to write logs to.
- maxBytes=10240: Rotates the log file after it reaches 10KB.
- backupCount=10: Keeps the 10 most recent log files.
- encoding='utf-8': Ensures proper handling of all characters.
"""
file_handler = RotatingFileHandler(
    'logs/app.log', 
    maxBytes=10240, 
    backupCount=10, 
    encoding='utf-8'
)

"""
Define the format for log messages.
Includes timestamp, log level, the message itself, and the file/line number.
"""
log_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
file_handler.setFormatter(log_formatter)

"""Set the logging level for the file handler (what messages it will process)."""
file_handler.setLevel(logging.INFO)

"""Attach the configured handler to the Flask application's logger."""
app.logger.addHandler(file_handler)

"""Set the overall logging level for the application."""
app.logger.setLevel(logging.INFO)

# --- 4. Blueprint Registration ---
from .users.views import users_bp 
app.register_blueprint(users_bp)

from .products import products_bp
# All routes in this blueprint will be prefixed with '/shop'
# e.g., /products/all -> /shop/all
app.register_blueprint(products_bp, url_prefix="/shop")

# --- 5. Root View Imports ---
from . import views