
import os
import psycopg2
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from urllib.parse import quote_plus
'''
REQUIRED FOR DATABASE CREATION ONLY, MAY DELETE ONCE COMPLETED
# from sqlalchemy import create_engine, text
# from sqlalchemy import create_engine
'''

from sqlalchemy.exc import IntegrityError

from sqlalchemy_utils import create_database


load_dotenv()
app = Flask(__name__)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST =  os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connection URL for the new database
password = quote_plus(DB_PASSWORD)
DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, nullable=True)


