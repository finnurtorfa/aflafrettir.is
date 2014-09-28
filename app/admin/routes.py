import os

from datetime import datetime

from flask import (render_template, redirect, url_for, flash, request, json,
                   session, current_app)
from flask.ext.login import login_required, current_user
from flask.ext.uploads import UploadNotAllowed

from facebook import FacebookAPI, GraphAPI

from helpers.text import remove_html_tags, slugify, get_all_imgs
from helpers.image import crop_image, jpeg_convert

from . import admin
from .forms import ProfileForm, PostForm, CategoryForm, AdForm, AboutForm

from .. import db, ads, imgs
from ..models import User, Post, Category, Image, About

### Profile Related Routes
##############################
@admin.route('/')
@admin.route('/profile', alias=True)
@login_required
def profile_index():
  return render_template('admin/user.html', user=current_user)

@admin.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
  form = ProfileForm()

  if form.validate_on_submit():
    current_user.name = form.name.data
    current_user.location = form.location.data
    current_user.bio = form.bio.data

    db.session.add(current_user._get_current_object())
    db.session.commit()

    flash("Síðan hefur verið uppfærð")

    return redirect(url_for('admin.profile_index'))

  form.name.data = current_user.name
  form.location.data = current_user.location
  form.bio.data = current_user.bio

  return render_template('admin/edit_user.html', form=form)

### News Related Routes
##############################

@admin.route('/facebook', methods=['GET', 'POST'])
@login_required
def post_to_fb():
  if current_user.fb_token:
    api = GraphAPI(current_user.fb_token)
  elif request.args.get('code'):
    f = FacebookAPI(current_app.config['FB_APP_ID'],
                    current_app.config['FB_APP_SECRET'],
                    url_for('admin.post_to_fb', 
                            _external=True))
    access_token = f.get_access_token(request.args.get('code'))
    user_access_token = access_token[b'access_token'].decode('utf-8')

    current_user.fb_token = user_access_token
    db.session.add(current_user)
    db.session.commit()

    api = GraphAPI(user_access_token)
  else:
    flash("Ekki tókst að senda póst á Facebook!")
    return redirect(url_for('admin.news_index'))

  accounts = api.get('me/accounts')

  for d in accounts['data']:
    if d['id'] == current_app.config['FB_PAGE_ID']:
      page_access_token = d['access_token']
      break
  else:
    flash("Ekki tókst að senda póst á Facebook!")
    return redirect(url_for('admin.news_index'))

  api = GraphAPI(page_access_token)
  post = api.post(current_app.config['FB_PAGE_ID'] + '/feed', 
                  params={'message': session.pop('body', None),
                          'link': session.pop('link', None),
                          'picture': session.pop('picture', None)})
  
  flash("Tókst að senda póst á Facebook")

  return redirect(url_for('admin.news_index'))

@admin.route('/news')
@login_required
def news_index():
  posts = Post.get_all()

  return render_template('admin/news.html', posts=posts)

@admin.route('/news/post', methods=['GET', 'POST'])
@login_required
def news_post():
  form = PostForm()
  form.category.choices = [(0, 'Almenn frétt')]
  form.created.data = datetime.utcnow()

  active = Category.get_all_active()

  form.category.choices.extend([(n+1, i.name) for n, i in enumerate(active)])

  if form.validate_on_submit():
    name = form.category.choices[int(form.category.data)][1]
    category = Category.get_by_name(name)

    post = Post(title=form.title.data,
                body=remove_html_tags(form.post.data),
                body_html=form.post.data, 
                timestamp=form.created.data, 
                author=current_user,
                category=category)

    db.session.add(post)
    db.session.commit()

    flash("Fréttin hefur verið vistuð!")


    if form.facebook.data:
      if current_user.fb_token:
        session['link'] = url_for('aflafrettir.post', 
                                  title=slugify(post.title),
                                  pid=post.id,
                                  _external=True)
        session['body'] = form.facebook.data
  
        return redirect(url_for('admin.post_to_fb'))
      else:
        f = FacebookAPI(current_app.config['FB_APP_ID'],
                        current_app.config['FB_APP_SECRET'],
                        url_for('admin.post_to_fb', 
                                _external=True))
        auth_url = f.get_auth_url(scope=['public_profile', 
                                         'email', 
                                         'manage_pages',
                                         'publish_actions'])

        session['link'] = url_for('aflafrettir.post', 
                                  title=slugify(post.title),
                                  pid=post.id,
                                  _external=True)
        session['body'] = form.facebook.data

        fn = os.path.basename(get_all_imgs(form.post.data)[0])
        session['picture'] = imgs.url(fn)

        return redirect(auth_url)
    
    return redirect(url_for('admin.news_index'))

  return render_template('admin/post.html', form=form)
  
@admin.route('/news/post/upload', methods=['GET', 'POST'])
@login_required
def nicedit_upload():
  file = request.files.get('image')
  filename = imgs.save(file)
  filename = jpeg_convert(imgs.path(filename))

  img = Image(filename=filename,
              location=url_for('static', filename='uploads/imgs/'),
              type=10,
              active=False)

  db.session.add(img)
  db.session.commit()

  crop_image(imgs.path(filename))
        
  links_dict  = {'original' : url_for('static', 
                                      filename='uploads/imgs/' + filename)}
  set_dict    = {'links' : links_dict}
  upload_dict = {'upload' : set_dict }

  return json.dumps(upload_dict)

@admin.route('/news/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def news_edit(post_id):
  post = Post.get_by_id(post_id)

  form = PostForm()
  form.category.choices = [(0, 'Almenn frétt')]

  active = Category.get_all_active()

  form.category.choices.extend([(n+1, i.name) for n, i in enumerate(active)])

  if form.validate_on_submit():
    name = form.category.choices[int(form.category.data)][1]
    category = Category.get_by_name(name)

    post.title      = form.title.data
    post.body       = remove_html_tags(form.post.data)
    post.body_html  = form.post.data
    post.timestamp  = form.created.data
    post.author     = current_user
    post.category   = category

    db.session.add(post)
    db.session.commit()

    flash("Fréttin hefur verið uppfærð!")

    return redirect(url_for('admin.news_index'))
  
  form.title.data       = post.title
  form.post.data        = post.body_html
  form.created.data     = post.timestamp
  form.category.data    = [i for i, v in enumerate(form.category.choices)
                             if v[1] == post.category.name][0]

  return render_template('admin/post.html', form=form)

@admin.route('/news/delete/<int:post_id>')
@login_required
def news_delete(post_id):
  post = Post.get_by_id(post_id)

  db.session.delete(post)
  db.session.commit()

  return redirect(url_for('admin.news_index'))

@admin.route('/news/category', methods=['GET', 'POST'])
@login_required
def news_category():
    form = CategoryForm()

    active = Category.get_all_active()
    inactive = Category.get_all_active(False)

    if active:
      form.active.choices = [(n, i.name) for n,i in enumerate(active)]
    else:
      form.active.choices = [(0, '')]

    if inactive:
      form.inactive.choices = [(n, i.name) for n,i in enumerate(inactive)]
    else:
      form.inactive.choices = [(0, '')]

    if request.method == 'POST':
      if form.submit.data and form.category.data:
        category = Category(name=form.category.data)

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.news_category'))

      if form.right.data and inactive and form.inactive.data != None:
        category_selected = form.inactive.choices[int(form.inactive.data)][1]
        category = Category.get_by_name(category_selected)
        category.active=True

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.news_category'))

      if form.left.data and active and form.active.data != None:
        category_selected = form.active.choices[int(form.active.data)][1]
        category = Category.get_by_name(category_selected)
        category.active=False

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.news_category'))

    return render_template('admin/category.html', form=form)

### File Upload Related Routes
##############################

@admin.route('/ad')
@login_required
def ad_index():
  form = AdForm()
  ads = Image.get_all_ads(only_active=False)

  return render_template('admin/ads.html', form=form, ads=ads)

@admin.route('/ad/upload', methods=['GET', 'POST'])
@login_required
def ad_upload():
  form = AdForm()

  if request.method == 'POST':
    if form.ad.data:
      try:
        file = request.files.get('ad')
        filename = ads.save(file)
        #filename = do_something(ads.path(filename))
        flash("Skráin hefur verið vistuð!")
      except UploadNotAllowed:
        flash("Ekki leyfileg tegund af skrá!")

        return redirect(url_for('admin.ad_index'))
      else:
        if form.url.data:
          if not form.url.data.startswith('http'):
            form.url.data = 'http://'+form.url.data

        ad = Image(filename=filename,
                   location=url_for('static', filename='uploads/ads/'),
                   type=form.placement.data,
                   url=form.url.data,
                   active=form.active.data)

        db.session.add(ad)
        db.session.commit()
        
        return redirect(url_for('admin.ad_index'))

  return render_template('admin/upload.html', form=form)

@admin.route('/ad/edit/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def ad_edit(ad_id):
  form = AdForm()
  ad = Image.get_by_id(ad_id)

  if request.method == 'POST':
    if form.url.data:
      if not form.url.data.startswith('http'):
        form.url.data = 'http://'+form.url.data

    ad.type      = form.placement.data
    ad.url       = form.url.data
    ad.active    = form.active.data

    db.session.add(ad)
    db.session.commit()

    flash("Auglýsingin hefur verið uppfærð")
    return redirect(url_for('admin.ad_index'))

  form.placement.data = ad.type
  form.url.data       = ad.url
  form.active.data    = ad.active

  return render_template('admin/upload.html', form=form)

@admin.route('/ad/delete/<int:ad_id>')
@login_required
def ad_delete(ad_id):
  import os

  ad = Image.get_by_id(ad_id)

  os.remove(ads.path(ad.filename))

  db.session.delete(ad)
  db.session.commit()

  flash("Auglýsingin hefur verið fjarlægð")

  return redirect(url_for('admin.ad_index'))

### About the page related routes
##############################
@admin.route('/about', methods=['GET', 'POST'])
def about():
  form = AboutForm()
  about = About().query.first() or About()

  if request.method == 'POST':
    about.body = form.body.data
    about.timestamp = datetime.utcnow()

    db.session.add(about)
    db.session.commit()

  form.body.data = about.body
  
  return render_template('admin/about.html', form=form)
