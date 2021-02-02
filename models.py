"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

    def update_info(self, first_name, last_name, image_url):
        """Update a users info"""
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url


