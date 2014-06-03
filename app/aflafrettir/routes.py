from flask import render_template

from . import aflafrettir

@aflafrettir.route('/')
def index():
  return render_template('aflafrettir/index.html')

@talks.route('/user/<username>')
def user(username):
 return render_template('aflafrettir/index.html', username = username)
