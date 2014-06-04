from flask import render_template

from . import aflafrettir
from ..models import User

@aflafrettir.route('/')
def index():
  return render_template('aflafrettir/index.html')

@aflafrettir.route('/user/<username>')
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('aflafrettir/user.html', username = username)
