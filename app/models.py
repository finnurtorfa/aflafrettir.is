from datetime import datetime

from . import db

class User(db.Model):
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
  member_since  = db.Column(db.DateTime(), default = datetime.uctnow)
