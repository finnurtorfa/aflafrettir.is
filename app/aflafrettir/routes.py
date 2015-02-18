import os

from flask import render_template, url_for, redirect, request, g, current_app
from flask.ext.mail import Message

from . import aflafrettir
from .forms import ContactForm, SearchForm
from ..models import User, Category, Post, About, Image

from .. import mail, imgs, babel

from helpers.text import get_thumbnail, time_ago


@babel.localeselector
def get_locale():
  return request.view_args.get('lang_code', 'is')


@aflafrettir.before_request
def before_request():
  g.search_form = SearchForm()


@aflafrettir.errorhandler(404)
def page_not_found(e):
  categories = Category.get_all_active()
  ads = Image.get_all_ads()
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

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
  categories = Category.get_all_active()
  posts = Post.get_per_page(page, current_app.config['POSTS_PER_PAGE'])
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  main_lg = [ad for ad in ads if ad.type == 1]
  main_sm = [ad for ad in ads if ad.type == 2]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

  for post in posts.items:
    f, e = get_thumbnail(post.body_html)
    fn = current_app.config['UPLOADS_DEFAULT_DEST'] + '/imgs/' + e

    distance_in_time = time_ago(post.timestamp)
    post.distance_in_time = distance_in_time
    post.thumbnail = imgs.url(e)

    if not e:
      post.thumbnail = url_for('static', filename='imgs/default.png')
    if not os.path.isfile(fn):
      post.thumbnail = url_for('static', filename='imgs/default.png')

  return render_template('aflafrettir/index.html',
                          categories=categories,
                          posts=posts,
                          top_ads=top_ads,
                          main_lg=main_lg,
                          main_sm=main_sm,
                          right_ads=right_ads,
                          left_ads=left_ads)


@aflafrettir.route('/frettir/flokkur/<int:cid>')
@aflafrettir.route('/frettir/flokkur/<int:cid>/sida/<int:page>')
@aflafrettir.route('/<lang_code>/frettir/flokkur/<int:cid>')
@aflafrettir.route('/<lang_code>/frettir/flokkur/<int:cid>/sida/<int:page>')
def category(cid, page=1, lang_code='is'):
  categories = Category.get_all_active()
  posts = Post.get_by_category(cid, page, current_app.config['POSTS_PER_PAGE'])
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  main_lg = [ad for ad in ads if ad.type == 1]
  main_sm = [ad for ad in ads if ad.type == 2]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

  for post in posts.items:
    f, e = get_thumbnail(post.body_html)
    fn = current_app.config['UPLOADS_DEFAULT_DEST'] + '/imgs/' + e

    distance_in_time = time_ago(post.timestamp)
    post.distance_in_time = distance_in_time
    post.thumbnail = imgs.url(e)

    if not e:
      post.thumbnail = url_for('static', filename='imgs/default.png')
    if not os.path.isfile(fn):
      post.thumbnail = url_for('static', filename='imgs/default.png')

  return render_template('aflafrettir/index.html',
                          categories=categories,
                          posts=posts,
                          top_ads=top_ads,
                          main_lg=main_lg,
                          main_sm=main_sm,
                          right_ads=right_ads,
                          left_ads=left_ads)


@aflafrettir.route('/frettir/grein/<title>/<int:pid>')
@aflafrettir.route('/<lang_code>/frettir/grein/<title>/<int:pid>')
def post(title, pid, lang_code='is'):
  post = Post.get_by_id(pid)
  categories = Category.get_all_active()
  ads = Image.get_all_ads()
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

  return render_template('aflafrettir/post.html',
                          categories=categories,
                          post=post,
                          right_ads=right_ads,
                          left_ads=left_ads)


@aflafrettir.route('/frettir/leita', methods=['POST'])
@aflafrettir.route('/<lang_code>/frettir/leita', methods=['POST'])
def search():
  if not g.search_form.validate_on_submit():
    return redirect(url_for('aflafrettir.index'))

  return redirect(url_for('aflafrettir.results',
                  query=g.search_form.search.data))


@aflafrettir.route('/frettir/leita/<query>')
@aflafrettir.route('/frettir/leita/<query>/sida/<int:page>')
@aflafrettir.route('/<lang_code>/frettir/leita/<query>')
@aflafrettir.route('/<lang_code>/frettir/leita/<query>/sida/<int:page>')
def results(query, page=1, lang_code='is'):
  categories = Category.get_all_active()
  posts = Post.search(query, page, current_app.config['POSTS_PER_PAGE'])
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  main_lg = [ad for ad in ads if ad.type == 1]
  main_sm = [ad for ad in ads if ad.type == 2]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

  for post in posts.items:
    f, e = get_thumbnail(post.body_html)
    fn = current_app.config['UPLOADS_DEFAULT_DEST'] + '/imgs/' + e

    distance_in_time = time_ago(post.timestamp)
    post.distance_in_time = distance_in_time
    post.thumbnail = imgs.url(e)

    if not e:
      post.thumbnail = url_for('static', filename='imgs/default.png')
    if not os.path.isfile(fn):
      post.thumbnail = url_for('static', filename='imgs/default.png')

  return render_template('aflafrettir/index.html',
                          categories=categories,
                          posts=posts,
                          top_ads=top_ads,
                          main_lg=main_lg,
                          main_sm=main_sm,
                          right_ads=right_ads,
                          left_ads=left_ads)


@aflafrettir.route('/um-siduna')
@aflafrettir.route('/<lang_code>/um-siduna')
def about(lang_code='is'):
  about = About.query.first()
  categories = Category.get_all_active()
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

  return render_template('aflafrettir/about.html',
                          about=about,
                          categories=categories,
                          top_ads=top_ads,
                          right_ads=right_ads,
                          left_ads=left_ads)


@aflafrettir.route('/hafa-samband', methods=['GET', 'POST'])
@aflafrettir.route('/<lang_code>/hafa-samband', methods=['GET', 'POST'])
def contact(lang_code='is'):
  form = ContactForm()
  categories = Category.get_all_active()
  ads = Image.get_all_ads()
  top_ads = [ad for ad in ads if ad.type == 0]
  right_ads = [ad for ad in ads if ad.type == 3]
  left_ads = [ad for ad in ads if ad.type == 4]

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
                          left_ads=left_ads)


@aflafrettir.route('/notandi/<username>')
@aflafrettir.route('/<lang_code>/notandi/<username>')
def user(username, lang_code='is'):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('aflafrettir/user.html', user=user)
