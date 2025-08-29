
import os
import psycopg2
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

load_dotenv()