import os

from flask import (render_template, url_for, redirect, request, g,
                   current_app, abort)
from flask_mail import Message

from . import aflafrettir
from .forms import ContactForm, SearchForm
from ..models import User, Category, Post, About, Image

from .. import mail, imgs, babel

from helpers.text import get_all_imgs, get_thumbnail, time_ago, slugify

@babel.localeselector
def get_locale():
  if request.view_args:
    return request.view_args.get('lang_code', 'is')

  return 'is'

@aflafrettir.before_app_request
def before_request():
  g.search_form = SearchForm()

  if request.view_args and 'lang_code' in request.view_args:
    if request.view_args['lang_code'] not in ('en', 'is'):
      return abort(404)

@aflafrettir.errorhandler(404)
def page_not_found(e):
  categories = Category.get_all_active()
  ads = Image.get_all_ads()
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

  current_app.logger.warning('{} for url {}'.format(e, request.url))

  return render_template('aflafrettir/404.html',
                         categories=categories,
                         right_ads=right_ads,
                         left_ads=left_ads), 404

@aflafrettir.route('/', alias=True)
@aflafrettir.route('/frettir')
@aflafrettir.route('/frettir/<int:page>')
@aflafrettir.route('/<lang_code>/frettir')
@aflafrettir.route('/<lang_code>/frettir/<int:page>')
def index(page=1, lang_code='is'):
  if '.com' in request.url:
    lang_code = 'en'

  categories = Category.get_all_active()
  posts = Post.get_per_page(page,
                            current_app.config['POSTS_PER_PAGE'],
                            lang=lang_code)
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  main_lg = [ad for ad in ads if ad.type == 1]
  main_sm = [ad for ad in ads if ad.type == 2]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

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
                         categories=categories,
                         posts=posts,
                         top_ads=top_ads,
                         main_lg=main_lg,
                         main_sm=main_sm,
                         right_ads=right_ads,
                         left_ads=left_ads,
                         lang_code=lang_code)

@aflafrettir.route('/frettir/flokkur/<int:cid>')
@aflafrettir.route('/frettir/flokkur/<int:cid>/sida/<int:page>')
@aflafrettir.route('/<lang_code>/frettir/flokkur/<int:cid>')
@aflafrettir.route('/<lang_code>/frettir/flokkur/<int:cid>/sida/<int:page>')
def category(cid, page=1, lang_code='is'):
  if '.com' in request.url:
    lang_code = 'en'

  categories = Category.get_all_active()
  posts = Post.get_by_category(cid,
                               page,
                               current_app.config['POSTS_PER_PAGE'],
                               lang=lang_code)
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  main_lg = [ad for ad in ads if ad.type == 1]
  main_sm = [ad for ad in ads if ad.type == 2]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

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
                         categories=categories,
                         posts=posts,
                         top_ads=top_ads,
                         main_lg=main_lg,
                         main_sm=main_sm,
                         right_ads=right_ads,
                         left_ads=left_ads,
                         lang_code=lang_code)

@aflafrettir.route('/frettir/grein/<title>/<int:pid>')
@aflafrettir.route('/<lang_code>/frettir/grein/<title>/<int:pid>')
def post(title, pid, lang_code='is'):
  if '.com' in request.url:
    lang_code = 'en'

  p = Post.get_by_id(pid)
  categories = Category.get_all_active()
  ads = Image.get_all_ads()
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]
  body_imgs = [os.path.basename(img) for img in get_all_imgs(p.body_html)]

  if title.encode('utf-8') != slugify(p.title):
    return abort(404)

  if lang_code == 'is':
    lang_code = None

  return render_template('aflafrettir/post.html',
                         categories=categories,
                         post=p,
                         right_ads=right_ads,
                         left_ads=left_ads,
                         lang_code=lang_code,
                         body_imgs=body_imgs)

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
  if '.com' in request.url:
    lang_code = 'en'

  categories = Category.get_all_active()
  posts = Post.search(query, page, current_app.config['POSTS_PER_PAGE'])
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  main_lg = [ad for ad in ads if ad.type == 1]
  main_sm = [ad for ad in ads if ad.type == 2]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

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
                         categories=categories,
                         posts=posts,
                         top_ads=top_ads,
                         main_lg=main_lg,
                         main_sm=main_sm,
                         right_ads=right_ads,
                         left_ads=left_ads,
                         lang_code=lang_code)

#pylint: disable-msg=E1101
@aflafrettir.route('/um-siduna')
@aflafrettir.route('/<lang_code>/um-siduna')
def about(lang_code='is'):
  if '.com' in request.url:
    lang_code = 'en'

  about_page = About.query.first()
  categories = Category.get_all_active()
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

  if lang_code == 'is':
    lang_code = None

  return render_template('aflafrettir/about.html',
                         about=about_page,
                         categories=categories,
                         top_ads=top_ads,
                         right_ads=right_ads,
                         left_ads=left_ads,
                         lang_code=lang_code)

@aflafrettir.route('/hafa-samband', methods=['GET', 'POST'])
@aflafrettir.route('/<lang_code>/hafa-samband', methods=['GET', 'POST'])
def contact(lang_code='is'):
  if '.com' in request.url:
    lang_code = 'en'

  form = ContactForm()
  categories = Category.get_all_active()
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

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
                         categories=categories,
                         top_ads=top_ads,
                         right_ads=right_ads,
                         left_ads=left_ads,
                         lang_code=lang_code)

@aflafrettir.route('/notandi/<username>')
@aflafrettir.route('/<lang_code>/notandi/<username>')
def user(username, lang_code='is'):
  if '.com' in request.url:
    lang_code = 'en'

  u = User.query.filter_by(username=username).first_or_404()

  if lang_code == 'is':
    lang_code = None

  return render_template('aflafrettir/user.html',
                         user=u,
                         lang_code=lang_code)
