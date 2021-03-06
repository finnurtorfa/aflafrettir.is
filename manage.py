import os

from app import create_app, db
from app.models import User, Category

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='127.0.0.1'))

#pylint: disable-msg=E1101
@manager.command
def adduser(email, username, admin=False):
  """ Register a new user"""
  from getpass import getpass
  password = getpass()
  password2 = getpass(prompt='Confirm: ')

  if password != password2:
    import sys
    sys.exit("Error: Passwords do not match!")

  db.create_all()

  category = Category.get_by_name('Almenn frétt')
  if category is None:
    category = Category(name='Almenn frétt',
                        name_en='General News',
                        active=True)
    db.session.add(category)

  user = User(email=email,
              username=username,
              password=password,
              is_admin=admin)
  db.session.add(user)
  db.session.commit()

  print('User {0} was registered successfully!'.format(username))

if __name__ == '__main__':
  manager.run()
