from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_user, logout_user, login_required

from . import auth
from .forms import LoginForm
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if user is None or not user.verify_password(form.password.data):
      flash('Rangt notendanafn eða lykilorð')
      return redirect(url_for('.login'))
    
    login_user(user, form.remember_me.data)

    return redirect(request.args.get('next') or url_for('admin.profile_index'))

  return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
  logout_user()
  flash('Þú hefur verið skráður út!')
  return redirect(url_for('aflafrettir.profile_index'))
