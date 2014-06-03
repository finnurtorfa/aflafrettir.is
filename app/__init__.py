from flask import Flask
from flask.ext.bootstrap import Bootstrap

from config import config

bootstrap = Bootstrap()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  bootstrap.init_app(app)

  from .aflafrettir import aflafrettir as afla_blueprint
  app.register_blueprint(afla_blueprint)

  return app
