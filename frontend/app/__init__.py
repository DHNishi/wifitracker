from flask import Flask
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload')
DATABASE = os.path.join(APP_ROOT, 'static/upload/packetDatabase.db')
ALLOWED_EXTENSIONS = set(['db'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['DATABASE'] = DATABASE
from app import server