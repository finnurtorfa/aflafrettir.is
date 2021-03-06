#pylint: disable-msg=R0903
from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
  email       = StringField('Email',
                            validators=[Required(), Length(1, 64), Email()])
  password    = PasswordField('Lykilorð', validators=[Required()])
  remember_me = BooleanField('Muna eftir mér?')
  submit      = SubmitField('Innskráning')
