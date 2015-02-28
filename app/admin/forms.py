from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, SelectField, \
                    DateTimeField, FileField, BooleanField
from wtforms.validators import Required, Length, Optional


class ProfileForm(Form):
  name      = StringField('Nafn', validators=[Optional(),
                                              Length(1, 64)])
  location  = StringField('Staðsetning', validators=[Optional(),
                                                     Length(1, 64)])
  bio       = TextAreaField('Um', validators=[Optional()])
  submit    = SubmitField('Breyta')


class PostForm(Form):
  title     = StringField('Titill', validators=[Required(),
                                                Length(1, 64)])
  created   = DateTimeField('Dagsetning', validators=[Optional()])
  post      = TextAreaField('Frétt', validators=[Required()])
  category  = SelectField('Flokkur', coerce=int, validators=[Optional()])
  facebook  = TextAreaField('Skilaboð á Facebook', validators=[Optional()])
  submit    = SubmitField('Senda')


class CategoryForm(Form):
  category  = StringField('Nafn á Flokki', validators=[Optional()])
  cat_en    = StringField('Enskt nafn', validators=[Optional()])
  submit    = SubmitField('Senda', validators=[Optional()])
  inactive  = SelectField('Flokkar sem ekki birtast', validators=[Optional()])
  right     = SubmitField('>', validators=[Optional()])
  left      = SubmitField('<', validators=[Optional()])
  active    = SelectField('Flokkar sem birtast', validators=[Optional()])


class AdForm(Form):
  ad        = FileField('Skrá', validators=[Required()])
  placement = SelectField('Staðsetning',
                          choices=[(0, 'Efst'),
                                   (1, 'Aðalhluti - Stór'),
                                   (2, 'Aðalhluti - Lítil'),
                                   (3, 'Til hægri'),
                                   (4, 'Til vinstri')],
                          coerce=int,
                          validators=[Required()])
  url       = StringField('Tengill', validators=[Optional()])
  active    = BooleanField('Auglýsing virk?', validators=[Required()])
  submit    = SubmitField('Vista')


class AboutForm(Form):
  body   = TextAreaField('Um síðuna', validators=[Required()])
  submit = SubmitField('Vista')
