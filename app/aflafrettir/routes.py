import os

from flask import render_template, url_for, redirect, request, g, current_app
from flask.ext.mail import Message

from . import aflafrettir
from .forms import ContactForm, SearchForm
from ..models import User, Category, Post, About

from .. import mail

from helpers.text import get_thumbnail, time_ago

@aflafrettir.before_app_request
def before_app_request():
  g.search_form = SearchForm()

@aflafrettir.route('/', alias=True)
@aflafrettir.route('/frettir')
@aflafrettir.route('/frettir/<int:page>')
def index(page=1):
  categories = Category.get_all_active()
  posts = Post.get_per_page(page, current_app.config['POSTS_PER_PAGE'])

  for post in posts.items:
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

    distance_in_time = time_ago(post.timestamp)
    post.distance_in_time = distance_in_time

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

@aflafrettir.route('/frettir/leita', methods=['POST'])
def search():
  if not g.search_form.validate_on_submit():
    return redirect(url_for('index'))

  return redirect(url_for('aflafrettir.results', query=g.search_form.search.data))

@aflafrettir.route('/frettir/leita/<query>')
def results(query):
  categories = Category.get_all_active()
  posts = Post.query.whoosh_search(query).all()

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


@aflafrettir.route('/um-siduna')
def about():
  about = About.query.first()
  return render_template('aflafrettir/about.html', about=about)

@aflafrettir.route('/hafa-samband', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if not form.validate():
      return render_template('aflafrettir/contact.html', form=form)
    else:
      msg = Message(form.subject.data, 
                    sender=form.email.data,
                    recipients=['finnurtorfa@gmail.com'],
                    charset='utf-8')
      print(mail)
      msg.body = """
      From: {n} <{e}>
      {s}
      """.format(n=form.name.data,
                 e=form.email.data,
                 s=form.message.data).encode('ascii', 'replace')

      mail.send(msg)

      return redirect(url_for('aflafrettir.contact'))

  return render_template('aflafrettir/contact.html', form=form)

@aflafrettir.route('/notandi/<username>')
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('aflafrettir/user.html', user=user)
