import os

from app import create_app, db
from app.models import User, Category

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


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
    category = Category(name='Almenn frétt', active=True)
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
