from app import db
from .base import Base

class User(Base):

    __tablename__ = 'user'

    # User Name
    name = db.Column(db.String(128),  nullable=False)

    # Sex
    sex = db.Column(db.String(128), nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)

    image_filename = db.Column(db.String, default=None, nullable=True)

    # Authorisation Data: role & status
    # role     = db.Column(db.SmallInteger, nullable=False)
    # status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, sex, password):

        self.name     = name
        self.sex      = sex
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)
