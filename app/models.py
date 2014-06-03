from datetime import datetime

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
  password_hash = db.Column(db.String(128))
  name          = db.Column(db.String(64))
  member_since  = db.Column(db.DateTime(), default = datetime.utcnow)

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
