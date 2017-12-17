import os

from datetime import datetime
from queue import Queue

from flask import (render_template, redirect, url_for, flash, request, json,
                   session, current_app, send_from_directory)
from flask_login import login_required, current_user
from flask_uploads import UploadNotAllowed

from facebook import GraphAPI

from helpers.text import remove_html_tags, slugify, get_all_imgs, truncate
from helpers.image import crop_image, jpeg_convert
from helpers.threading import run_in_thread, list_lock
from helpers.os_methods import get_all_files, remove_file

from . import admin
from .forms import (ProfileForm, PostForm, CategoryForm, AdForm, AboutForm,
                    ListForm)

from .. import db, ads, imgs, landings, afla_manager
from ..models import Post, Category, Image, About

list_queue = Queue()

@admin.before_app_request
def before_request():
  while not list_queue.empty():
    flash(list_queue.get())

"""Profile Related Routes
"""
@admin.route('/')
@admin.route('/profile', alias=True)
@login_required
def profile_index():
  categories = Category.get_all_active()
  return render_template('admin/user.html', categories=categories, user=current_user)

#pylint: disable-msg=E1101
@admin.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
  form = ProfileForm()
  categories = Category.get_all_active()

  if form.validate_on_submit():
    current_user.name = form.name.data
    current_user.location = form.location.data
    current_user.bio = form.bio.data

    db.session.add(current_user)
    db.session.commit()

    flash("Síðan hefur verið uppfærð")

    return redirect(url_for('admin.profile_index'))

  form.name.data = current_user.name
  form.location.data = current_user.location
  form.bio.data = current_user.bio

  return render_template('admin/edit_user.html', categories=categories, form=form)

"""News Related Routes
"""
@admin.route('/facebook', methods=['GET', 'POST'])
@login_required
def post_to_fb():
  if current_user.fb_token:
    current_app.logger.debug('User {} already has token: {}'
                             .format(current_user.username,
                                     current_user.fb_token))
    current_app.logger.debug(request.args)

    api = GraphAPI(current_user.fb_token, version='2.7')
  elif request.args.get('code'):
    current_app.logger.debug('Fetching Facebook token for user {}'
                             .format(current_user.username))
    current_app.logger.debug(request.args)
  else:
    current_app.logger.error("Not able to send post to Facebook for user {}"
                             .format(current_user.username))
    current_app.logger.error(request.args)

    flash("Ekki tókst að senda póst á Facebook!")
    return redirect(url_for('admin.news_index'))

  accounts = api.get_object('me/accounts')

  for d in accounts['data']:
    if d['id'] == current_app.config['FB_PAGE_ID']:
      page_access_token = d['access_token']
      break
  else:
    current_app.logger.error('Not able to find the page_access_token')
    current_app.logger.error(accounts)
    current_app.logger.error(current_app.config['FB_PAGE_ID'])
    flash("Ekki tókst að senda póst á Facebook!")

    return redirect(url_for('admin.news_index'))

  api = GraphAPI(page_access_token, version='2.7')
  api.put_object(parent_object=current_app.config['FB_PAGE_ID'],
                 connection_name='feed',
                 message=session.pop('body', None),
                 link=session.pop('link', None))

  #  flash("Tókst að senda póst á Facebook")
  #except GraphAPIError as e:
  #  flash("Tókst ekki að senda á Facebook. Skilaboð: {0}".format(e))

  return redirect(url_for('admin.news_index'))

@admin.route('/news')
@admin.route('/<lang>/news')
@login_required
def news_index(lang='is'):
  posts = Post.get_all(lang=lang)
  categories = Category.get_all_active()

  if lang == 'is':
    lang = None

  return render_template('admin/news.html',
                         categories=categories,
                         posts=posts,
                         lang=lang)

@admin.route('/news/post', methods=['GET', 'POST'])
@admin.route('/<lang>/news/post', methods=['GET', 'POST'])
@login_required
def news_post(lang='is'):
  form = PostForm()
  form.category.choices = [(0, 'Almenn frétt')]
  form.created.data = datetime.utcnow()
  categories = Category.get_all_active()

  if lang == 'is':
    lang = None

  active = Category.get_all_active()

  form.category.choices.extend([(n + 1, i.name) for n, i in enumerate(active)])

  if form.validate_on_submit():
    name = form.category.choices[int(form.category.data)][1]
    category = Category.get_by_name(name)

    post = Post(title=form.title.data,
                body=remove_html_tags(form.post.data),
                body_html=form.post.data,
                language=lang or 'is',
                timestamp=form.created.data,
                author=current_user,
                category=category)

    db.session.add(post)
    db.session.commit()

    flash("Fréttin hefur verið vistuð!")

    if form.facebook.data:
      try:
        fn = os.path.basename(get_all_imgs(form.post.data)[0])
        fn = current_app.config['UPLOADS_DEFAULT_DEST'] + '/imgs/' + fn
      except IndexError:
        fn = url_for('static', filename='imgs/facebook.png')

      if not os.path.isfile(fn):
        fn = url_for('static', filename='imgs/facebook.png')
      else:
        fn = imgs.url(os.path.basename(fn))

      session['link'] = url_for('aflafrettir.post',
                                title=slugify(post.title),
                                pid=post.id,
                                _external=True)
      session['body'] = form.facebook.data
      session['picture'] = fn
      session['name'] = form.title.data
      session['caption'] = truncate(form.post.data)

      current_app.logger.debug('Preparing data for Facebook')
      current_app.logger.debug(session)

      if current_user.fb_token:
        return redirect(url_for('admin.post_to_fb'))
      else:
        current_app.error("Need to get authentication")

    return redirect(url_for('admin.news_index', lang=lang))

  return render_template('admin/post.html',
                         categories=categories,
                         form=form,
                         lang=lang)

@admin.route('/news/post/upload', methods=['GET', 'POST'])
@login_required
def nicedit_upload():
  file = request.files.get('image')
  filename = imgs.save(file)
  filename = jpeg_convert(imgs.path(filename))

  current_app.logger.debug('Uploaded {} to the server'.format(filename))

  img = Image(filename=filename,
              ad_html=None,
              location=url_for('static', filename='uploads/imgs/'),
              type=10,
              active=False)

  db.session.add(img)
  db.session.commit()

  crop_image(imgs.path(filename))

  links_dict  = {'original': url_for('static',
                                     filename='uploads/imgs/' + filename)}
  set_dict    = {'links': links_dict}
  upload_dict = {'upload': set_dict}

  current_app.logger.debug('upload_dict {}'.format(upload_dict))

  return json.dumps(upload_dict)

@admin.route('/news/edit/<int:post_id>', methods=['GET', 'POST'])
@admin.route('/<lang>/news/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def news_edit(post_id, lang='is'):
  post = Post.get_by_id(post_id)
  categories = Category.get_all_active()

  if lang == 'is':
    lang = None

  form = PostForm()
  form.category.choices = [(0, 'Almenn frétt')]

  active = Category.get_all_active()

  form.category.choices.extend([(n + 1, i.name) for n, i in enumerate(active)])

  if form.validate_on_submit():
    name = form.category.choices[int(form.category.data)][1]
    category = Category.get_by_name(name)

    post.title      = form.title.data
    post.body       = remove_html_tags(form.post.data)
    post.body_html  = form.post.data
    post.language   = lang or 'is'
    post.timestamp  = form.created.data
    post.author     = current_user
    post.category   = category

    db.session.add(post)
    db.session.commit()

    flash("Fréttin hefur verið uppfærð!")

    return redirect(url_for('admin.news_index', lang=lang))

  form.title.data       = post.title
  form.post.data        = post.body_html
  form.created.data     = post.timestamp
  form.category.data    = [i for i, v in enumerate(form.category.choices)
                           if v[1] == post.category.name][0]

  return render_template('admin/post.html',
                         categories=categories,
                         form=form,
                         lang=lang)

@admin.route('/news/delete/<int:post_id>')
@admin.route('/<lang>/news/delete/<int:post_id>')
@login_required
def news_delete(post_id, lang='is'):
  post = Post.get_by_id(post_id)
  categories = Category.get_all_active()

  if lang == 'is':
    lang = None

  db.session.delete(post)
  db.session.commit()

  return redirect(url_for('admin.news_index', categories=categories, lang=lang))

@admin.route('/news/category', methods=['GET', 'POST'])
@login_required
def news_category():
    form = CategoryForm()
    categories = Category.get_all_active()

    active = Category.get_all_active()
    inactive = Category.get_all_active(False)

    if active:
      form.active.choices = [(n, i.name) for n, i in enumerate(active)]
    else:
      form.active.choices = [(0, '')]

    if inactive:
      form.inactive.choices = [(n, i.name) for n, i in enumerate(inactive)]
    else:
      form.inactive.choices = [(0, '')]

    if request.method == 'POST':
      if form.submit.data and form.category.data and form.cat_en.data:
        current_app.logger.debug('Adding a new category: {}, {}'
                                 .format(form.category.data, form.cat_en.data))

        category = Category(name=form.category.data,
                            name_en=form.cat_en.data)

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.news_category'))

      if form.right.data and inactive and form.inactive.data is not None:
        current_app.logger.debug('Deactivating category: {}'
                                 .format(form.category.data))

        category_selected = form.inactive.choices[int(form.inactive.data)][1]
        category = Category.get_by_name(category_selected)
        category.active = True

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.news_category'))

      if form.left.data and active and form.active.data is not None:
        current_app.logger.debug('Activating category: {}'
                                 .format(form.category.data))

        category_selected = form.active.choices[int(form.active.data)][1]
        category = Category.get_by_name(category_selected)
        category.active = False

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.news_category'))

    return render_template('admin/category.html', categories=categories, form=form)

"""File Upload Related Routes
"""
@admin.route('/ad')
@login_required
def ad_index():
  form = AdForm()
  all_ads = Image.get_all_ads(only_active=False)
  categories = Category.get_all_active()

  return render_template('admin/ads.html', categories=categories, form=form, ads=all_ads)

@admin.route('/ad/upload', methods=['GET', 'POST'])
@login_required
def ad_upload():
  form = AdForm()
  categories = Category.get_all_active()

  filename = None

  if request.method == 'POST':
    if form.ad.data or form.ad_html.data:
      if form.ad.data:
        try:
          file = request.files.get('ad')
          filename = ads.save(file)
          flash("Skráin hefur verið vistuð!")
        except UploadNotAllowed:
          current_app.logger.exception('Tried to upload {}'.format(file))

          flash("Ekki leyfileg tegund af skrá!")

          return redirect(url_for('admin.ad_index'))

      if form.url.data:
        if not form.url.data.startswith('http'):
          form.url.data = 'http://' + form.url.data

      ad = Image(filename=filename,
                 ad_html=form.ad_html.data,
                 location=url_for('static', filename='uploads/ads/'),
                 type=form.placement.data,
                 url=form.url.data,
                 active=form.active.data)

      db.session.add(ad)
      db.session.commit()

      return redirect(url_for('admin.ad_index'))

  return render_template('admin/upload.html', categories=categories, form=form)

@admin.route('/ad/edit/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def ad_edit(ad_id):
  form = AdForm()
  ad = Image.get_by_id(ad_id)
  categories = Category.get_all_active()

  if request.method == 'POST':
    if form.url.data:
      if not form.url.data.startswith('http'):
        form.url.data = 'http://' + form.url.data

    ad.type      = form.placement.data
    ad.ad_html  = form.ad_html.data
    ad.url       = form.url.data
    ad.active    = form.active.data

    db.session.add(ad)
    db.session.commit()

    flash("Auglýsingin hefur verið uppfærð")

    return redirect(url_for('admin.ad_index'))

  form.placement.data = ad.type
  form.ad_html.data    = ad.ad_html
  form.url.data       = ad.url
  form.active.data    = ad.active

  return render_template('admin/upload.html', categories=categories, form=form)

@admin.route('/ad/delete/<int:ad_id>')
@login_required
def ad_delete(ad_id):
  ad = Image.get_by_id(ad_id)

  if ad.filename:
    os.remove(ads.path(ad.filename))

  db.session.delete(ad)
  db.session.commit()

  flash("Auglýsingin hefur verið fjarlægð")

  return redirect(url_for('admin.ad_index'))

"""About the page related routes
"""
@admin.route('/about', methods=['GET', 'POST'])
@login_required
def about():
  form = AboutForm()
  my_about = About().query.first() or About()
  categories = Category.get_all_active()

  if request.method == 'POST':
    my_about.body = form.body.data
    my_about.timestamp = datetime.utcnow()

    db.session.add(my_about)
    db.session.commit()

  form.body.data = my_about.body

  return render_template('admin/about.html', categories=categories, form=form)

""" Informatics and Analytics
"""
@admin.route('/info/google')
@login_required
def google():
  return render_template('admin/google.html')

""" Aflafrettir extension
"""
@admin.route('/list', methods=['GET', 'POST'])
@admin.route('/list/<path:filename>', methods=['GET', 'POST'])
@login_required
def make_list(filename=None):
  form = ListForm()
  files = get_all_files(landings.config.destination)
  categories = Category.get_all_active()

  if filename is not None:
    if os.path.isfile(landings.path(filename)):
      return send_from_directory(filename=filename,
                                 directory=landings.config.destination)

  if request.method == 'POST':
    if form.validate_on_submit():
      make_list_in_thread(app=current_app._get_current_object(),
                          name=landings.path(form.name.data),
                          date_from=form.date_from.data,
                          date_to=form.date_to.data)

      flash('Er að útbúa lista. Aðgerðin getur tekið nokkurn tíma!')
      return redirect(url_for('admin.make_list'))

  return render_template('admin/list.html', categories=categories, form=form, files=files)

@admin.route('/list/delete/<path:filename>/')
@login_required
def delete_list(filename):
  remove_file(filename, landings.config.destination)
  
  return redirect(url_for('admin.make_list'))

@run_in_thread(current_app)
def make_list_in_thread(app, name, date_from, date_to):
  if list_lock.locked():
    list_queue.put('Get aðeins útbúið einn lista í senn!')
    app.logger.info('Thread already started, exiting!')
  else:
    app.logger.info('Acquiring a lock for making lists!')
    list_lock.acquire()
    try:
      if afla_manager.make_list(name=name,
                                date_from=date_from,
                                date_to=date_to):
        app.logger.info('The list is ready')
      else:
        app.logger.error('Something happened! Try again')
    finally:
      list_queue.put('Listinn er tilbúinn!')
      app.logger.info('Releasing a lock for making lists')
      list_lock.release()
