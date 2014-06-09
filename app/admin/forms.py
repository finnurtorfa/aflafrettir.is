from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
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
  created   = DateField('Dagsetning', validators=[Optional()])
  post      = TextAreaField('Frétt', validators=[Required()])
  category  = SelectField('Flokkur', coerce=int, validators=[Optional()])
  submit    = SubmitField('Senda')

