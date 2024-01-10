"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User {u.first_name}-{u.last_name}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50),
                          nullable=False)

    image_url = db.Column(db.String(100),
                          default='images/img.jpg')

    posts = db.relationship('Post')


class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<Post --{p.title}-->"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime,
                           nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')

    tags = db.relationship('Tag',
                           secondary="posttags"
                           #                          backref="posts"
                           )


class Tag(db.Model):
    __tablename__ = 'tags'

    def __repr__(self):
        return f"<Tag --{self.name}-->"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(30),
                     nullable=False)

    posts = db.relationship('Post',
                            secondary="posttags"
                            #                            backref="tags"
                            )


class PostTag(db.Model):
    __tablename__ = 'posttags'

    def __repr__(self):
        return "<PostTag>"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)
