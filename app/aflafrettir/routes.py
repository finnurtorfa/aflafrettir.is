from flask import render_template

from . import aflafrettir
from ..models import User, Category, Post

@aflafrettir.route('/')
def index():
  categories = Category.get_all_active()
  posts = Post.get_all()
  return render_template('aflafrettir/index.html', 
                         categories=categories,
                         posts=posts)

@aflafrettir.route('/user/<username>')
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('aflafrettir/user.html', user=user)
