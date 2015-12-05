import os

from flask import (render_template, url_for, redirect, request, g,
                   current_app, abort)
from flask_mail import Message

from . import aflafrettir
from .forms import ContactForm, SearchForm
from ..models import User, Category, Post, About, Image

from .. import mail, imgs, babel

from helpers.text import get_thumbnail, time_ago, slugify

@babel.localeselector
def get_locale():
  if request.view_args:
    return request.view_args.get('lang_code', 'is')

  return 'is'

""" This function will be called before every request in the application and do
some preprocessing.
"""
@aflafrettir.before_app_request
def before_app_request():
  g.search_form = SearchForm()
  g.categories = Category.get_all_active()

  if request.view_args and 'lang_code' in request.view_args:
    if request.view_args['lang_code'] not in ('en', 'is'):
      return abort(404)

""" This function will be run before every request made within the aflafrettir
blueprint context and do some necessary preprocessing.
"""
@aflafrettir.before_request
def before_aflafrettir_bp_request():
  ads = Image.get_all_ads()
  g.top_ads = [ad for ad in ads if ad.type == 0]
  g.main_lg = [ad for ad in ads if ad.type == 1]
  g.main_sm = [ad for ad in ads if ad.type == 2]
  g.right_ads = [ad for ad in ads if ad.type == 3]
  g.left_ads = [ad for ad in ads if ad.type == 4]

@aflafrettir.errorhandler(404)
def page_not_found(e):
  current_app.logger.warning('{} for url {}'.format(e, request.url))

  return render_template('aflafrettir/404.html'), 404

@aflafrettir.route('/', alias=True)
@aflafrettir.route('/frettir')
@aflafrettir.route('/frettir/<int:page>')
@aflafrettir.route('/<lang_code>/frettir')
@aflafrettir.route('/<lang_code>/frettir/<int:page>')
def index(page=1, lang_code='is'):
  posts = Post.get_per_page(page,
                            current_app.config['POSTS_PER_PAGE'],
                            lang=lang_code)
  if lang_code == 'is':
    lang_code = None

  for p in posts.items:
    _, e = get_thumbnail(p.body_html)
    fn = current_app.config['UPLOADS_DEFAULT_DEST'] + '/imgs/' + e

    distance_in_time = time_ago(p.timestamp)
    p.distance_in_time = distance_in_time
    p.thumbnail = imgs.url(e)

    if not e:
      p.thumbnail = url_for('static', filename='imgs/default.png')
    if not os.path.isfile(fn):
      p.thumbnail = url_for('static', filename='imgs/default.png')

  return render_template('aflafrettir/index.html',
                         posts=posts,
                         lang_code=lang_code)

@aflafrettir.route('/frettir/flokkur/<int:cid>')
@aflafrettir.route('/frettir/flokkur/<int:cid>/sida/<int:page>')
@aflafrettir.route('/<lang_code>/frettir/flokkur/<int:cid>')
@aflafrettir.route('/<lang_code>/frettir/flokkur/<int:cid>/sida/<int:page>')
def category(cid, page=1, lang_code='is'):
  posts = Post.get_by_category(cid,
                               page,
                               current_app.config['POSTS_PER_PAGE'],
                               lang=lang_code)
  if lang_code == 'is':
    lang_code = None

  for p in posts.items:
    _, e = get_thumbnail(p.body_html)
    fn = current_app.config['UPLOADS_DEFAULT_DEST'] + '/imgs/' + e

    distance_in_time = time_ago(p.timestamp)
    p.distance_in_time = distance_in_time
    p.thumbnail = imgs.url(e)

    if not e:
      p.thumbnail = url_for('static', filename='imgs/default.png')
    if not os.path.isfile(fn):
      p.thumbnail = url_for('static', filename='imgs/default.png')

  return render_template('aflafrettir/index.html',
                         posts=posts,
                         lang_code=lang_code)

@aflafrettir.route('/frettir/grein/<title>/<int:pid>')
@aflafrettir.route('/<lang_code>/frettir/grein/<title>/<int:pid>')
def post(title, pid, lang_code='is'):
  p = Post.get_by_id(pid)

  if title.encode('utf-8') != slugify(p.title):
    return abort(404)

  if lang_code == 'is':
    lang_code = None

  return render_template('aflafrettir/post.html',
                         post=p,
                         lang_code=lang_code)

@aflafrettir.route('/frettir/leita', methods=['POST'])
@aflafrettir.route('/<lang_code>/frettir/leita', methods=['POST'])
def search(lang_code='is'):
  if not g.search_form.validate_on_submit():
    return redirect(url_for('aflafrettir.index',
                            lang_code=lang_code))

  return redirect(url_for('aflafrettir.results',
                          query=g.search_form.search.data,
                          lang_code=lang_code))

@aflafrettir.route('/frettir/leita/<query>')
@aflafrettir.route('/frettir/leita/<query>/sida/<int:page>')
@aflafrettir.route('/<lang_code>/frettir/leita/<query>')
@aflafrettir.route('/<lang_code>/frettir/leita/<query>/sida/<int:page>')
def results(query, page=1, lang_code='is'):
  posts = Post.search(query, page, current_app.config['POSTS_PER_PAGE'])

  if lang_code == 'is':
    lang_code = None

  for p in posts.items:
    _, e = get_thumbnail(p.body_html)
    fn = current_app.config['UPLOADS_DEFAULT_DEST'] + '/imgs/' + e

    distance_in_time = time_ago(p.timestamp)
    p.distance_in_time = distance_in_time
    p.thumbnail = imgs.url(e)

    if not e:
      p.thumbnail = url_for('static', filename='imgs/default.png')
    if not os.path.isfile(fn):
      p.thumbnail = url_for('static', filename='imgs/default.png')

  return render_template('aflafrettir/index.html',
                         posts=posts,
                         lang_code=lang_code)

#pylint: disable-msg=E1101
@aflafrettir.route('/um-siduna')
@aflafrettir.route('/<lang_code>/um-siduna')
def about(lang_code='is'):
  about_page = About.query.first()

  if lang_code == 'is':
    lang_code = None

  return render_template('aflafrettir/about.html',
                         about=about_page,
                         lang_code=lang_code)

@aflafrettir.route('/hafa-samband', methods=['GET', 'POST'])
@aflafrettir.route('/<lang_code>/hafa-samband', methods=['GET', 'POST'])
def contact(lang_code='is'):
  form = ContactForm()

  if lang_code == 'is':
    lang_code = None

  if request.method == 'POST':
    if not form.validate():
      return render_template('aflafrettir/contact.html', form=form)
    else:
      msg = Message(form.subject.data,
                    sender=form.email.data,
                    recipients=[current_app.config['MAIL_USERNAME']],
                    charset='utf-8')
      msg.body = """
      From: {n} <{e}>
      {s}
      """.format(n=form.name.data,
                 e=form.email.data,
                 s=form.message.data)

      mail.send(msg)

      return redirect(url_for('aflafrettir.contact'))

  return render_template('aflafrettir/contact.html',
                         form=form,
                         lang_code=lang_code)

@aflafrettir.route('/notandi/<username>')
@aflafrettir.route('/<lang_code>/notandi/<username>')
def user(username, lang_code='is'):
  u = User.query.filter_by(username=username).first_or_404()

  if lang_code == 'is':
    lang_code = None

  return render_template('aflafrettir/user.html',
                         user=u,
                         lang_code=lang_code)
