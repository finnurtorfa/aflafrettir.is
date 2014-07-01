from datetime import datetime

from flask import render_template, redirect, url_for, flash, request, json
from flask.ext.login import login_required, current_user
from flask.ext.uploads import UploadNotAllowed

from helpers.text import remove_html_tags

from . import admin
from .forms import ProfileForm, PostForm, CategoryForm, AdForm

from .. import db, ads, imgs
from ..models import User, Post, Category, Image

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

    return redirect(url_for('admin.news_index'))

  return render_template('admin/post.html', form=form)
  
@admin.route('/news/post/upload', methods=['GET', 'POST'])
@login_required
def nicedit_upload():
  file = request.files.get('image')
  filename = imgs.save(file)

  img = Image(filename=filename,
              location=url_for('static', filename='uploads/imgs/'),
              type=4,
              active=False)

  db.session.add(img)
  db.session.commit()
        
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
  form.post.data        = post.body
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
  ads = Image.get_all_ads()

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
        flash("Skráin hefur verið vistuð!")
      except UploadNotAllowed:
        flash("Ekki leyfileg tegund af skrá!")

        return redirect(url_for('admin.ad_index'))
      else:
        ad = Image(filename=filename,
                   location=url_for('static', filename='uploads/ads/'),
                   type=form.placement.data,
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
    ad.type      = form.placement.data
    ad.active    = form.active.data

    db.session.add(ad)
    db.session.commit()

    flash("Auglýsingin hefur verið uppfærð")
    return redirect(url_for('admin.ad_index'))

  form.placement.data = ad.type
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
