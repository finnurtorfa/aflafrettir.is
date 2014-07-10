import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  CSRF_ENABLED = True
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'my secret key'
  UPLOADS_DEFAULT_DEST = os.environ.get('UPLOADS_DEFAULT_DEST') or \
          basedir + '/app/static/uploads'
  MAIL_SERVER   = os.environ.get('MAIL_SERVER') or 'smtp.gmal.com'
  MAIL_PORT     = os.environ.get('MAIL_POST') or 465
  MAIL_USE_SSL  = os.environ.get('MAIL_USE_SSL') or True
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'user@mail.com'
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'some_password'

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
          'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
  IMAGE_DELETE = { 'TIME_OF_DAY': [i for i in range(24)],
                   'WEEKDAY': [i for i in range(7)] }

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
          'sqlite:///' + os.path.join(basedir, 'test-dev.sqlite')

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
          'sqlite:///' + os.path.join(basedir, 'data.sqlite')
  IMAGE_DELETE = { 'TIME_OF_DAY': [3, 4],
                   'WEEKDAY': [0] }

config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig,
  'default': DevelopmentConfig
}
