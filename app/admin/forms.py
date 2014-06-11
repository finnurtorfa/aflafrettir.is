from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, SelectField, \
                    DateTimeField, FileField, BooleanField
from wtforms.validators import Required, Length, Email, Optional

class ProfileForm(Form):
  name      = StringField('Nafn', validators=[Optional(),
                                              Length(1,64)])
  location  = StringField('Staðsetning', validators=[Optional(), 
                                                     Length(1,64)])
  bio       = TextAreaField('Um', validators=[Optional()])
  submit    = SubmitField('Breyta')

class PostForm(Form):
  title     = StringField('Titill', validators=[Required(), 
                                                Length(1,64)])
  created   = DateTimeField('Dagsetning', validators=[Optional()])
  post      = TextAreaField('Frétt', validators=[Required()])
  category  = SelectField('Flokkur', coerce=int, validators=[Optional()])
  submit    = SubmitField('Senda')

class CategoryForm(Form):
  category  = StringField('Nafn á Flokki', validators=[Optional()])
  submit    = SubmitField('Senda', validators=[Optional()])
  inactive  = SelectField('Flokkar sem ekki birtast', validators=[Optional()])
  right     = SubmitField('>', validators=[Optional()])
  left      = SubmitField('<', validators=[Optional()])
  active    = SelectField('Flokkar sem birtast', validators=[Optional()])

class AdForm(Form):
  ad        = FileField('Skrá', validators=[Required()])
  placement = SelectField('Staðsetning', 
                          choices=[(0, ' '),
                                   (1, 'Efst'),
                                   (2, 'Aðalhluti'),
                                   (3, 'Til vinstri'),
                                   (4, 'Til hægri')],
                          coerce=int,
                          validators=[Required()])
  active    = BooleanField('Auglýsing virk?', validators=[Required()])
  submit    = SubmitField('Vista')

