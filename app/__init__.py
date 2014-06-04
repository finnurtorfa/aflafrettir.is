from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  bootstrap.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)

  from .aflafrettir import aflafrettir as afla_blueprint
  from .auth import auth as auth_blueprint
  from .admin import admin as admin_blueprint
  app.register_blueprint(afla_blueprint)
  app.register_blueprint(auth_blueprint, url_prefix='/auth')
  app.register_blueprint(admin_blueprint, url_prefix='/admin')

  return app
