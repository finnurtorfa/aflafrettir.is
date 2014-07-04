import os

from flask import render_template, url_for

from . import aflafrettir
from ..models import User, Category, Post

from helpers.text import get_thumbnail, time_ago

@aflafrettir.route('/frettir')
@aflafrettir.route('/', alias=True)
def index():
  categories = Category.get_all_active()
  posts = Post.get_all()

  for post in posts:
    f, e = get_thumbnail(post.body_html)
    fn = f + '/' + e

    distance_in_time = time_ago(post.timestamp)
    post.distance_in_time = distance_in_time

    if not e and not os.path.isfile(fn):
      post.thumbnail = url_for('static', filename='imgs_default/fish1.jpg')
    else:
      post.thumbnail = fn
      
  return render_template('aflafrettir/index.html', 
                         categories=categories,
                         posts=posts)

@aflafrettir.route('/frettir/flokkur/<int:cid>')
def category(cid):
  categories = Category.get_all_active()
  posts = Post.get_by_category(cid)

  for post in posts:
    f, e = get_thumbnail(post.body_html)
    fn = f + '/' + e

    if not e and not os.path.isfile(fn):
      post.thumbnail = url_for('static', filename='imgs_default/fish1.jpg')
    else:
      post.thumbnail = fn
      
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
