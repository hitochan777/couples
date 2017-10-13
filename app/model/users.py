from app import db
from .base import Base

class User(Base):

    __tablename__ = 'users'

    # User Name
    name = db.Column(db.String(128),  nullable=False)

    # Sex
    sex = db.Column(db.String(128), nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)

    image_filename = db.Column(db.String, default=None, nullable=True)

    image_url = db.Column(db.String, default=None, nullable=True)

    # New instance instantiation procedure
    def __init__(self, name, email, sex, password, image_filename, image_url):

        self.name     = name
        self.sex      = sex
        self.email    = email
        self.password = password
        self.image_filename = image_filename
        self.image_url = image_url

    def __repr__(self):
        return '<User %r>' % (self.name)
