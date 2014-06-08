from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_required, current_user

from . import admin
from .forms import ProfileForm

from .. import db
from ..models import User

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
  return render_template('admin/news.html')
