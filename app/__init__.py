import logging
import logging.config

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
from flask_whooshalchemy import whoosh_index
from flask_babel import Babel
from flask_aflafrettir import Aflafrettir

from helpers.text import slugify, truncate

from config import config

bootstrap = Bootstrap()

db = SQLAlchemy()
mail = Mail()
babel = Babel()
aflafrettir = Aflafrettir()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

ads = UploadSet('ads', IMAGES)
imgs = UploadSet('imgs', IMAGES)

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  configure_logging()

  app.jinja_env.globals.update(slugify=slugify)
  app.jinja_env.globals.update(truncate=truncate)
  app.jinja_env.globals.update(url=ads.url)

  bootstrap.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)
  configure_uploads(app, (ads, imgs))
  mail.init_app(app)
  babel.init_app(app)
  aflafrettir.init_app(app)

  from .models import Post
  whoosh_index(app, Post)

  from .aflafrettir import aflafrettir as afla_blueprint
  from .auth import auth as auth_blueprint
  from .admin import admin as admin_blueprint
  from .rss import feed as feed_blueprint
  app.register_blueprint(afla_blueprint)
  app.register_blueprint(auth_blueprint, url_prefix='/auth')
  app.register_blueprint(admin_blueprint, url_prefix='/admin')
  app.register_blueprint(feed_blueprint, url_prefix='/feed')

  from helpers.image import start_image_deletion_thread

  #pylint: disable-msg=W0612
  @app.before_first_request
  def before_first_request():
    start_image_deletion_thread()

  return app

def configure_logging(logger='logger.yml'):
  import os, yaml

  try:
    os.makedirs('log', exist_ok=True)
  except OSError:
    logging.exception('OSError: ')

  if os.path.exists(logger):
    with open(logger) as f:
      conf = yaml.load(f.read())

  logging.config.dictConfig(conf)

class LevelFilter(logging.Filter):
  def __init__(self, level):
    super(LevelFilter, self).__init__()
    self.__level = level

  def filter(self, record):
    return record.levelno == self.get_level()

  def get_level(self):
    return self.__level
