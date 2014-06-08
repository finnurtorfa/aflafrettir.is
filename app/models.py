import hashlib 

from datetime import datetime

from flask import request
from flask.ext.login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email         = db.Column(db.String(64), 
                            nullable=False, 
                            unique=True, 
                            index=True)
  username      = db.Column(db.String(64), 
                            nullable=False, 
                            unique=True, 
                            index=True)
  is_admin      = db.Column(db.Boolean)
  name          = db.Column(db.String(64))
  location      = db.Column(db.String(64))
  bio           = db.Column(db.Text())
  password_hash = db.Column(db.String(128))
  avatar_hash   = db.Column(db.String(32))
  member_since  = db.Column(db.DateTime(), default = datetime.utcnow)
  posts         = db.relationship('Post', backref='author', lazy='dynamic')

  def __init__(self, **kwargs):
    super(User, self).__init__(**kwargs)

    if self.email is not None and self.avatar_hash is None:
        self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

  @property
  def password(self):
    raise AttributeError('Password is not a readable attribute')

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))
  
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def gravatar(self, size=100, default='identicon', rating='g'):
    if request.is_secure:
      url = 'https://secure.gravatar.com/avatar'
    else:
      url = 'http://www.gravatar.com/avatar'

    hash = self.avatar_hash or \
           hashlib.md5(self.email.encode('utf-8')).hexdigest()

    return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url,
                                                                 hash=hash,
                                                                 size=size,
                                                                 default=default,
                                                                 rating=rating)

class Post(db.Model):
  __tablename__ = 'posts'
  id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title         = db.Column(db.String(64))
  body          = db.Column(db.Text)
  body_html     = db.Column(db.Text)
  timestamp     = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  author_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
