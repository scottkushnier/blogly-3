"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime
import sys

app = Flask(__name__)
testing = 'unittest' in sys.modules
if not testing:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly-3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly-3-test'
    app.config['SQLALCHEMY_ECHO'] = False
connect_db(app)


@app.route('/')
def home_page():
    return (redirect('/users/'))


@app.route('/users/')
def users_page():
    users = User.query.all()
    sorted_users = sorted(users, key=lambda x: x.last_name + x.first_name)
    return (render_template('home.html', is_userlist=True, users=sorted_users))


@app.route('/users/new/')
def new_user_page():
    return (render_template('home.html', newuser=True))


@app.route('/users/new/', methods=['POST'])
def new_user_post_page():
    first_name = request.form.get('first')
    last_name = request.form.get('last')
    image_file = request.form.get('image')
    if (image_file != ''):
        new_user = User(first_name=first_name,
                        last_name=last_name, image_url=image_file)
    else:
        new_user = User(first_name=first_name,
                        last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    print(new_user)

    return (redirect('/users/'))


@app.route('/users/<int:id>/')
def user_page(id):
    user = User.query.get(id)
    posts = user.posts
    print('HERE IS USER', id, user)
    return (render_template('home.html', user=user, posts=posts))


@app.route('/users/<int:id>/edit/')
def edit_user_page(id):
    user = User.query.get(id)
    return (render_template('home.html', edit_user=user))


@app.route('/users/<int:id>/edit/', methods=['POST'])
def edit_user_post_page(id):
    user = User.query.get(id)
    user.first_name = request.form.get('first')
    user.last_name = request.form.get('last')
    user.image_url = request.form.get('image')
    db.session.add(user)
    db.session.commit()
    return (redirect(f"/users/{id}/"))


@app.route('/users/<int:id>/delete/')
def delete_post_page(id):
    user = User.query.get(id)
    print(user)
    db.session.delete(user)
    db.session.commit()
    return (redirect('/users/'))


@app.route('/posts/<int:post_id>/delete/')
def delete_user_post_page(post_id):
    post = Post.query.get(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return (redirect(f'../../../users/{user_id}'))


@app.route('/posts/<int:id>/')
def post_page(id):
    post = Post.query.get(id)
    return (render_template('home.html', post=post, tags=sorted(post.tags, key=lambda x: x.name)))


@app.route('/users/<int:id>/posts/new/')
def new_post_page(id):
    sorted_tags = sorted(Tag.query.all(), key=lambda x: x.name)
    return (render_template('home.html', new_post=True, new_post_user=User.query.get(id),
                            tags=sorted_tags))


@app.route('/posts/<int:id>/edit/')
def edit_post_page(id):
    post = Post.query.get(id)
    sorted_tags = sorted(Tag.query.all(), key=lambda x: x.name)
    return (render_template('home.html', edit_post=post, tags=post.tags, all_tags=sorted_tags))


@app.route('/posts/<int:id>/edit/', methods=['POST'])
def edit_post_post_page(id):      # for editing a user's post, this is the POST page
    post = Post.query.get(id)
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    db.session.add(post)
    db.session.commit()
    # remove all tags for this post first,
    PostTag.query.filter_by(post_id=id).delete()
    db.session.commit()
    for tag_id in request.form.getlist('tags'):     # then add proper ones
        post_tag = PostTag(tag_id=tag_id, post_id=post.id)
        db.session.add(post_tag)
    db.session.commit()
    return (redirect(f"/posts/{id}/"))


@app.route('/users/<int:id>/posts/new/', methods=['POST'])
def new_post_post_page(id):      # for inserting a new post, this is the POST page
    post = Post()
    print('new post for', id)
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    post.user_id = id
    post.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.add(post)
    db.session.commit()
    for tag_id in request.form.getlist('tags'):
        post_tag = PostTag(tag_id=tag_id, post_id=post.id)
        db.session.add(post_tag)
    db.session.commit()
    print(request.form.getlist('tags'))
    return (redirect(f"/users/{id}/"))


@app.route('/tags/')
def tags_page():
    tags = Tag.query.all()
    sorted_tags = sorted(tags, key=lambda x: x.name)
    return (render_template('home.html', is_taglist=True, tags=sorted_tags))


@app.route('/tags/new/')
def new_tag_page():
    return (render_template('home.html', newtag=True))


@app.route('/tags/new/', methods=['POST'])
def new_tag_post_page():
    name = request.form.get('name')
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return (redirect('/tags/'))


@app.route('/tags/<int:id>/')
def post_tag(id):
    tag = Tag.query.get(id)
    return (render_template('home.html', tag=tag))


@app.route('/tags/<int:id>/edit/')
def edit_tag(id):
    tag = Tag.query.get(id)
    return (render_template('home.html', edit_tag=tag))


@app.route('/tags/<int:id>/edit/', methods=['POST'])
def edit_tag_post_page(id):      # for editing a user's post, this is the POST page
    tag = Tag.query.get(id)
    tag.name = request.form.get('name')
    db.session.add(tag)
    db.session.commit()
    return (redirect(f"/tags/"))


@app.route('/tags/<int:id>/delete/')
def delete_tag(id):
    tag = Tag.query.get(id)
    print('delete tag', tag.id)
    # first delete all posttags with that tag
    PostTag.query.filter_by(tag_id=id).delete()
    db.session.commit()
    # then delete tag
    db.session.delete(tag)
    db.session.commit()
    return (redirect(f"/tags/"))

##########################################################


def seed():
    Post.query.delete()
    db.session.commit()
    User.query.delete()
    db.session.commit()

    barney = User(first_name='Barney', last_name='Rubble',
                  image_url="images/barney.jpg")
    betty = User(first_name='Betty', last_name='Rubble',
                 image_url="images/betty.jpg")
    mrslate = User(first_name='George', last_name='Slate')
    db.session.add(barney)
    db.session.add(betty)
    db.session.add(mrslate)
    db.session.commit()

    p1 = Post(title='First Post', content='hello world',
              created_at='2024-1-1 14:05', user_id=barney.id)
    p2 = Post(title='Next Post', content='are you there?',
              created_at='2024-1-1 14:15', user_id=barney.id)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
