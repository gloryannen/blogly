"""Blogly application."""

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db
from routes import bp_routes

app = Flask(__name__)
app.register_blueprint(bp_routes)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shhitsasecret!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()