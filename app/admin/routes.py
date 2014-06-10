from datetime import datetime

from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_required, current_user

from . import admin
from .forms import ProfileForm, PostForm, CategoryForm

from .. import db
from ..models import User, Post, Category

@admin.route('/')
@login_required
def index():
  return render_template('admin/user.html', user=current_user)

@admin.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
  form = ProfileForm()

  if form.validate_on_submit():
    current_user.name = form.name.data
    current_user.location = form.location.data
    current_user.bio = form.bio.data

    db.session.add(current_user._get_current_object())
    db.session.commit()

    flash("Síðan hefur verið uppfærð")

    return redirect(url_for('admin.index'))

  form.name.data = current_user.name
  form.location.data = current_user.location
  form.bio.data = current_user.bio

  return render_template('admin/edit_user.html', form=form)

@admin.route('/news')
@login_required
def news():
  posts = Post.get_all()

  return render_template('admin/news.html', posts=posts)

@admin.route('/news/post', methods=['GET', 'POST'])
@login_required
def post():
  form = PostForm()
  form.category.choices = [(0, 'Almenn frétt')]
  form.created.data = datetime.utcnow()

  active = Category.get_all_active()

  form.category.choices.extend([(n+1, i.name) for n, i in enumerate(active)])

  if form.validate_on_submit():
    name = form.category.choices[int(form.category.data)][1]
    category = Category.get_by_name(name)

    post = Post(title=form.title.data,
                body=form.post.data, 
                body_html=form.post.data, 
                timestamp=form.created.data, 
                author=current_user,
                category=category)

    db.session.add(post)
    db.session.commit()

    flash("Fréttin hefur verið vistuð!")

    return redirect(url_for('admin.news'))

  return render_template('admin/post.html', form=form)
  
@admin.route('/news/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
  post = Post.get_by_id(post_id)

  form = PostForm()
  form.category.choices = [(0, 'Almenn frétt')]

  active = Category.get_all_active()

  form.category.choices.extend([(n+1, i.name) for n, i in enumerate(active)])

  if form.validate_on_submit():
    name = form.category.choices[int(form.category.data)][1]
    category = Category.get_by_name(name)

    post.title      = form.title.data
    post.body       = form.post.data
    post.body_html  = form.post.data
    post.timestamp  = form.created.data
    post.author     = current_user
    post.category   = category

    db.session.add(post)
    db.session.commit()

    flash("Fréttin hefur verið uppfærð!")

    return redirect(url_for('admin.news'))
  
  form.title.data       = post.title
  form.post.data        = post.body
  form.created.data     = post.timestamp
  form.category.data    = [i for i, v in enumerate(form.category.choices)
                             if v[1] == post.category.name][0]

  return render_template('admin/post.html', form=form)

@admin.route('/news/category', methods=['GET', 'POST'])
@login_required
def category():
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

        return redirect(url_for('admin.category'))

      if form.right.data and inactive and form.inactive.data != None:
        category_selected = form.inactive.choices[int(form.inactive.data)][1]
        category = Category.get_by_name(category_selected)
        category.active=True

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.category'))

      if form.left.data and active and form.active.data != None:
        category_selected = form.active.choices[int(form.active.data)][1]
        category = Category.get_by_name(category_selected)
        category.active=False

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.category'))

    return render_template('admin/category.html', form=form)
