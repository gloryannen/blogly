'''Models for Blogly.'''

import datetime
from flask_sqlalchemy import SQLAlchemy

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
                          nullable=True)

    posts = db.relationship('Post',
                            cascade='all, delete-orphan',
                            backref='user')

    def __repr__(self):
        return f'<User {self.id}, {self.first_name}, {self.last_name}>'


class Post(db.Model):
    '''Post Model'''

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True)

    title = db.Column(db.String(30),
                      nullable=False)

    content = db.Column(db.String,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    def __repr__(self):
        return f'<Post ID-{self.id}, Title-{self.title}, Content-{self.content} Created-{self.created_at} User ID -{self.user_id}>'

    @property
    def formatted_datetime(self):
        return self.created_at.strftime('%a %b %-d, %Y at %-I:%M %p')


class PostTag(db.Model):
    '''PostTag Model'''

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)

    def __repr__(self):
        return f'<PostTag postid {self.post_id}, tagid {self.tag_id}>'


class Tag(db.Model):
    '''Tag Model'''

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.Text,
                     unique=True,
                     nullable=False)

    posts = db.relationship('Post',
                            secondary='posts_tags',
                            backref='tags')

    def __repr__(self):
        return f'<Tag {self.id}, {self.name}>'
