import hashlib 

from datetime import datetime

from flask import request
from flask.ext.login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import desc

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

    return '{u}/{h}?s={s}&d={d}&r={r}'.format(u=url,
                                              h=hash,
                                              s=size,
                                              d=default,
                                              r=rating)

class Post(db.Model):
  __tablename__ = 'posts'
  id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title         = db.Column(db.String(64))
  body          = db.Column(db.Text)
  body_html     = db.Column(db.Text)
  timestamp     = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  author_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
  category_id   = db.Column(db.Integer, db.ForeignKey('categories.id'))

  @classmethod
  def get_all(cls, descending=True):
    if descending:
      return cls.query.order_by(cls.timestamp.desc()).all()
    else:
      return cls.query.order_by(cls.timestamp).all()

  @classmethod
  def get_by_id(cls, aid):
    return cls.query.filter_by(id=aid).first()

  @classmethod
  def get_by_category(cls, cid):
    return cls.query.filter(cls.category_id == cid).all()

class Category(db.Model):
  __tablename__ = 'categories'
  id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name          = db.Column(db.String(64), nullable=False, unique=True)
  active        = db.Column(db.Boolean, nullable=False, default=False)
  posts         = db.relationship('Post', backref='category', lazy='dynamic')
  
  @classmethod
  def get_all_active(cls, active=True):
    if active:
      return cls.query.filter_by(active=True)\
              .filter(cls.name != 'Almenn frétt').all()
    else:
      return cls.query.filter_by(active=False)\
             .filter(cls.name != 'Almenn frétt').all()

  @classmethod
  def get_by_name(cls, name):
    return cls.query.filter_by(name=name).first()
  
class Ad(db.Model):
  __tablename__  = 'ads'
  id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
  filename       = db.Column(db.String(120), nullable=False)
  placement      = db.Column(db.Integer, nullable=False)
  active         = db.Column(db.Boolean, default=False)
  timestamp      = db.Column(db.DateTime, 
                             nullable=False,
                             default=datetime.utcnow)
 
  @classmethod
  def get_all(cls, descending=True):
    if descending:
      return cls.query.order_by(cls.timestamp.desc()).all()
    else:
      return cls.query.order_by(cls.timestamp).all()

  @classmethod
  def get_by_id(cls, aid):
    return cls.query.filter_by(id=aid).first()

