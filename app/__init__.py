from flask import Flask
from config import config

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  from .aflafrettir import aflafrettir as afla_blueprint
  app.register_blueprint(afla_blueprint)

  return app
