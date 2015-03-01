import hashlib

from datetime import datetime

from flask import request
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager

#pylint: disable-msg=E1101
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

#pylint: disable-msg=E1101
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
  bio           = db.Column(db.Text)
  password_hash = db.Column(db.String(128))
  avatar_hash   = db.Column(db.String(32))
  member_since  = db.Column(db.DateTime(), default = datetime.utcnow)
  fb_token      = db.Column(db.Text)
  posts         = db.relationship('Post', backref='author', lazy='dynamic')

  def __init__(self, **kwargs):
    super(User, self).__init__(**kwargs)

    if self.email is not None and self.avatar_hash is None:
        self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

  #pylint: disable-msg=R0201
  @property
  def password(self):
    raise AttributeError('Password is not a readable attribute')

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

    h = self.avatar_hash or \
        hashlib.md5(self.email.encode('utf-8')).hexdigest()

    return '{u}/{h}?s={s}&d={d}&r={r}'.format(u=url,
                                              h=h,
                                              s=size,
                                              d=default,
                                              r=rating)

class Post(db.Model):
  __tablename__ = 'posts'
  __searchable__ = ['title', 'body_html']

  id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title         = db.Column(db.String(64))
  body          = db.Column(db.Text)
  body_html     = db.Column(db.Text)
  language      = db.Column(db.String(4), default='is')
  timestamp     = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  author_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
  category_id   = db.Column(db.Integer, db.ForeignKey('categories.id'))

  def __init__(self, **kwargs):
    super(Post, self).__init__(**kwargs)

  @classmethod
  def get_all(cls, descending=True, lang='is'):
    if descending:
      return cls.query.order_by(cls.timestamp.desc())\
                .filter_by(language=lang)\
                .all()
    else:
      return cls.query.order_by(cls.timestamp)\
                .filter_by(language=lang)\
                .all()

  @classmethod
  def get_per_page(cls, page, per_page=5, descending=True, lang='is'):
    if descending:
      return cls.query.order_by(cls.timestamp.desc())\
                .filter_by(language=lang)\
                .paginate(page, per_page, False)
    else:
      return cls.query.order_by(cls.timestamp)\
                .filter_by(language=lang)\
                .paginate(page, per_page, False)

  @classmethod
  def get_by_id(cls, aid):
    return cls.query.filter_by(id=aid).first_or_404()

  #pylint: disable-msg=R0913
  @classmethod
  def get_by_category(cls, cid, page, per_page=5, descending=True, lang='is'):
    if descending:
      return cls.query.filter(cls.category_id == cid)\
                .filter_by(language=lang)\
                .order_by(cls.timestamp.desc())\
                .paginate(page, per_page, False)
    else:
      return cls.query.filter(cls.category_id == cid)\
                .filter_by(language=lang)\
                .order_by(cls.timestamp)\
                .paginate(page, per_page, False)

  @classmethod
  def search(cls, query, page, per_page=4, descending=True):
    if descending:
      return cls.query.whoosh_search(query)\
                .order_by(cls.timestamp.desc())\
                .paginate(page, per_page, False)
    else:
      return cls.query.whoosh_search(query)\
                .order_by(cls.timestamp)\
                .paginate(page, per_page, False)


class Category(db.Model):
  __tablename__ = 'categories'
  id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name          = db.Column(db.String(64), nullable=False, unique=True)
  name_en       = db.Column(db.String(64), nullable=False, unique=True)
  active        = db.Column(db.Boolean, nullable=False, default=False)
  posts         = db.relationship('Post', backref='category', lazy='dynamic')

  def __init__(self, **kwargs):
    super(Category, self).__init__(**kwargs)

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

class Image(db.Model):
  __tablename__  = 'images'
  id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
  filename       = db.Column(db.String(120), nullable=False)
  location       = db.Column(db.String(120), nullable=False)
  type           = db.Column(db.Integer, nullable=False)
  url            = db.Column(db.String(120))
  active         = db.Column(db.Boolean, default=False)
  timestamp      = db.Column(db.DateTime,
                             nullable=False,
                             default=datetime.utcnow)

  def __init__(self, **kwargs):
    super(Image, self).__init__(**kwargs)

  @classmethod
  def get_all_imgs(cls, descending=True):
    if descending:
      return cls.query.filter(cls.type >= 10)\
                      .order_by(cls.timestamp.desc()).all()
    else:
      return cls.query.filter(cls.type >= 10)\
                      .order_by(cls.timestamp).all()

  @classmethod
  def get_all_ads(cls, descending=True, only_active=True):
    if descending:
      if only_active:
        return cls.query.filter(cls.type < 10)\
                        .filter(cls.active == True)\
                        .order_by(cls.timestamp.desc()).all()
      else:
        return cls.query.filter(cls.type < 10)\
                        .order_by(cls.timestamp.desc()).all()
    else:
      if only_active:
        return cls.query.filter(cls.type < 10)\
                        .filter(cls.active == True)\
                        .order_by(cls.timestamp).all()
      else:
        return cls.query.filter(cls.type < 10)\
                        .order_by(cls.timestamp).all()

  @classmethod
  def get_by_id(cls, aid):
    return cls.query.filter_by(id=aid).first()

#pylint: disable-msg=R0903
class About(db.Model):
  __tablename__ = 'about'
  id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
  body          = db.Column(db.Text)
  timestamp     = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)

  def __init__(self, **kwargs):
    super(About, self).__init__(**kwargs)

