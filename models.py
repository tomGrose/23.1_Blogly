"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    def __repr__(self):
        """ Show info about user"""
        return f"<User {self.first_name} {self.last_name}"

    

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(20),
                     nullable=False)
    last_name = db.Column(db.String(20),
                     nullable=False)
    image_url = db.Column(db.String(100), nullable=True,
                            default="http://www.newdesignfile.com/postpic/2014/07/generic-user-icon-windows_352871.png")

    post = db.relationship("Post", cascade="all, delete-orphan")

    def update_info(self, first_name, last_name, image_url):
        """Update a users info"""
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    def __repr__(self):
        """ Show info about a user's post"""
        return f"<User {self.title} created by {self.user_id}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(20),
                     nullable=False)
    content = db.Column(db.String(300),
                     nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, 
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))

    def update_post(self, title, content):
        """Update a post"""
        self.title = title
        self.content = content

    user = db.relationship( 'User', backref='posts')



