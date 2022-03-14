"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import table

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  '''User Model'''

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

  def __repr__(self):
        return f'<User {self.id}, {self.first_name}, {self.last_name}>'

class Post(db.Model):
  '''Post Model'''

  __tablename__ = 'posts'

  id = db.Column(db.Integer,
                 primary_key=True,
                 autoincrement=True)

  title = db.Column(db.String(15),
                  nullable=False)

  content = db.Column(db.String,
                  nullable=False)

  created_at = db.Column(db.DateTime,
                  nullable=False,
                  default = datetime.datetime.now)

  user_id = db.Column(db.Integer,
                   db.ForeignKey('users.id'))

  user = db.relationship('User', backref='posts')

  def __repr__(self):
    return f'<Post {self.id}, {self.title}, {self.content}>'

  @property
  def formatted_datetime(self):
    return self.created_at.strftime('%a %b %-d, %Y at %-I:%M %p')