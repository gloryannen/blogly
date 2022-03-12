"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import table

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  '''User'''

  __tablename__ = 'users'

  @property
  def full_name(self):
    return f'{self.first_name} {self.last_name}'

  id = db.Column(db.Integer,
                 primary_key=True,
                 autoincrement=True)

  first_name = db.Column(db.String(15),
                  nullable=False)

  last_name = db.Column(db.String(15),
                  nullable=False)

  image_url = db.Column(db.Text,
                  nullable=True )