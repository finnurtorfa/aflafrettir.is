from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from flask.ext.mail import Mail
from flask.ext.whooshalchemy import whoosh_index

from helpers.text import slugify, truncate

from config import config

bootstrap = Bootstrap()

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

ads = UploadSet('ads', IMAGES)
imgs = UploadSet('imgs', IMAGES)

mail = Mail()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  app.jinja_env.globals.update(slugify=slugify)
  app.jinja_env.globals.update(truncate=truncate)
  app.jinja_env.globals.update(url=ads.url)

  bootstrap.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)
  configure_uploads(app, (ads, imgs))
  mail.init_app(app)

  from .models import Post
  whoosh_index(app, Post)

  from .aflafrettir import aflafrettir as afla_blueprint
  from .auth import auth as auth_blueprint
  from .admin import admin as admin_blueprint
  app.register_blueprint(afla_blueprint)
  app.register_blueprint(auth_blueprint, url_prefix='/auth')
  app.register_blueprint(admin_blueprint, url_prefix='/admin')

  from helpers.image import start_image_deletion_thread
  @app.before_first_request
  def before_first_request():
    start_image_deletion_thread()

  return app
