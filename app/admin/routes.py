from datetime import datetime

from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_required, current_user

from . import admin
from .forms import ProfileForm, PostForm

from .. import db
from ..models import User, Post

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
  print(posts)

  return render_template('admin/news.html', posts=posts)

@admin.route('/news/post', methods=['GET', 'POST'])
@login_required
def post():
  form = PostForm()
  form.category.choices = [(0, 'Almenn frétt')]
  form.created.data = datetime.utcnow()

  if form.validate_on_submit():

    post = Post(title=form.title.data,
                body=form.post.data, 
                body_html=form.post.data, 
                timestamp=form.created.data, 
                author=current_user)

    db.session.add(post)
    db.session.commit()

    flash("Fréttin hefur verið vistuð!")
    return redirect(url_for('admin.news'))

  return render_template('admin/post.html', form=form)
