from flask import render_template

from . import aflafrettir
from ..models import User, Category, Post

@aflafrettir.route('/frettir')
@aflafrettir.route('/', alias=True)
def index():
  categories = Category.get_all_active()
  posts = Post.get_all()
  return render_template('aflafrettir/index.html', 
                         categories=categories,
                         posts=posts)

@aflafrettir.route('/frettir/flokkur/<int:cid>')
def category(cid):
  categories = Category.get_all_active()
  posts = Post.get_by_category(cid)
  return render_template('aflafrettir/index.html', 
                          categories=categories,
                          posts=posts)

@aflafrettir.route('/frettir/grein/<title>/<int:pid>')
def post(title, pid):
  post = Post.get_by_id(pid)
  categories = Category.get_all_active()
  return render_template('aflafrettir/post.html', 
                          categories=categories,
                          post=post)

@aflafrettir.route('/user/<username>')
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('aflafrettir/user.html', user=user)
