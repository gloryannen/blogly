"""Blogly application."""

from crypt import methods
import re
from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shhitsasecret!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    '''Home page'''
    return redirect('/users')

@app.route('/users')
def list_users():
  ''''Show all users, link to user pages, and link to add user'''

  users = User.query.order_by(User.last_name.asc()).all()
  return render_template('users_list.html', users=users)

@app.route('/users/new', methods=['GET'])
def show_user_form():
  '''Show form to add users'''

  return render_template('user_create_form.html')

@app.route('/users/new', methods=['POST'])
def add_user_form():
  '''Handle user creation'''

  # Set field values and create new user on SQLAlchemy from them
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  image_url = request.form['image_url']

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

  db.session.add(new_user)
  db.session.commit()

  return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def user_information(user_id):
  '''Display user information'''

  user = User.query.get_or_404(user_id)
  posts = Post.query.all()
  user_post = user.posts

  return render_template('user_details.html', user=user, user_post=user_post)

@app.route('/users/<int:user_id>/edit', methods=['GET'])
def load_user_information(user_id):
  '''Load user information'''

  user = User.query.get_or_404(user_id)
  return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_information(user_id):
  '''Edit user information'''

  user = User.query.get_or_404(user_id)

  # If a field is not modified, leave as its current value, otherwise update it accordingly
  if request.form['first_name'] != '':
    user.first_name = request.form['first_name']
  if request.form['last_name'] != '':
    user.last_name = request.form['last_name']
  if request.form['image_url'] != '':
    user.image_url = request.form['image_url']

  db.session.commit()

  return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['GET','POST'])
def delete_user(user_id):
  '''Delete user'''

  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()

  return redirect ('/users')

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def load_post_form(user_id):
  '''Show form to add users'''

  user = User.query.get_or_404(user_id)

  return render_template('post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_post_form(user_id):
  '''Handle user post creation'''

  user = User.query.get_or_404(user_id)
  # Set field values and create new user on SQLAlchemy from them
  title = request.form['title']
  content = request.form['content']

  new_post = Post(title=title, content=content, user_id=user.id)

  db.session.add(new_post)
  db.session.commit()

  return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>', methods=['GET'])
def load_post_information(post_id):
  '''Load post information'''

  post = Post.query.get_or_404(post_id)
  return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post_details(post_id):
  '''Edit post details'''

  post = Post.query.get_or_404(post_id)
  return render_template('post_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
  '''Handle edit post'''

  post = Post.query.get_or_404(post_id)
  # If a field is not modified, leave as its current value, otherwise update it accordingly
  if request.form['title'] != '':
    post.title = request.form['title']
  if request.form['content'] != '':
    post.content = request.form['content']

  db.session.commit()

  return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['GET','POST'])
def delete_post(post_id):
  '''Delete user'''

  post = Post.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()

  return redirect (f'/users/{post.user_id}')