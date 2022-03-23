from flask import Blueprint, render_template, redirect, request
from models import db, User, Post, Tag

bp_routes = Blueprint('/bp_routes', __name__, template_folder='templates')

# region User Routes


@bp_routes.route('/')
@bp_routes.route('/home')
def home_page():
    '''Home page'''

    posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()

    return render_template('home.html', posts=posts)


@bp_routes.route('/users')
def list_users():
    ''''Show all users, link to user pages, and link to add user'''

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users_list.html', users=users)


@bp_routes.route('/users/new', methods=['GET'])
def show_user_form():
    '''Show form to add users'''

    return render_template('user_create_form.html')


@bp_routes.route('/users/new', methods=['POST'])
def add_user_form():
    '''Handle user creation'''

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')


@bp_routes.route('/users/<int:user_id>')
def user_information(user_id):
    '''Display user information'''

    user = User.query.get_or_404(user_id)

    return render_template('user_details.html', user=user)


@bp_routes.route('/users/<int:user_id>/edit', methods=['GET'])
def load_user_information(user_id):
    '''Load user information'''

    user = User.query.get_or_404(user_id)

    return render_template('user_edit.html', user=user)


@bp_routes.route('/users/<int:user_id>/edit', methods=['POST'])
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

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@bp_routes.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Delete user'''

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# endregion

# region Post routes


@bp_routes.route('/users/<int:user_id>/posts/new', methods=['GET'])
def load_post_form(user_id):
    '''Show form to add users'''

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('post_form.html', user=user, tags=tags)


@bp_routes.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_post_form(user_id):
    '''Handle user post creation'''

    user = User.query.get_or_404(user_id)
    tag_ids = [int(t) for t in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@bp_routes.route('/posts/<int:post_id>', methods=['GET'])
def load_post_information(post_id):
    '''Load post information'''

    post = Post.query.get_or_404(post_id)

    return render_template('post_details.html', post=post)


@bp_routes.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post_details(post_id):
    '''Edit post details'''

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post_edit.html', post=post, tags=tags)


@bp_routes.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
    '''Handle edit post'''

    post = Post.query.get_or_404(post_id)
    if request.form['title'] != '':
        post.title = request.form['title']
    if request.form['content'] != '':
        post.content = request.form['content']

    tag_ids = [int(t) for t in request.form.getlist('tag')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


@bp_routes.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Delete user'''

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

# endregion

# region Tag routes


@bp_routes.route('/tags', methods=['GET'])
def show_tags():
    '''Show list of tags'''

    tags = Tag.query.all()

    return render_template('tag_list.html', tags=tags)


@bp_routes.route('/tags/new', methods=['GET'])
def show_tag_form():
    '''Show form to add tags'''

    posts = Post.query.all()

    return render_template('tag_form.html', posts=posts)


@bp_routes.route('/tags/new', methods=['POST'])
def add_tag_form():
    '''Handle tag creation'''

    post_ids = [int(p) for p in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()

    new_tag = Tag(name=request.form['name'],
                  posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect(f'/tags')


@bp_routes.route('/tags/<int:tag_id>', methods=['GET'])
def tag_details(tag_id):
    '''Load tag details'''

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_details.html', tag=tag)


@bp_routes.route('/tags/<int:tag_id>/edit', methods=['GET'])
def load_tag_information(tag_id):
    '''Load tag information'''

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template('tag_edit.html', tag=tag, posts=posts)


@bp_routes.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag_information(tag_id):
    '''Edit tag information'''

    tag = Tag.query.get_or_404(tag_id)

    if request.form['name'] != '':
        tag.name = request.form['name']

    post_ids = [int(p) for p in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@bp_routes.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''Delete tag'''

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect(f'/tags')

# endregion
