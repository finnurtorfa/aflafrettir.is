from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Length, Email, Optional

class ProfileForm(Form):
  name      = StringField('Nafn', validators=[Optional(),
                                              Length(1,64)])
  location  = StringField('Staðsetning', validators=[Optional(), 
                                                     Length(1,64)])
  bio       = TextAreaField('Um', validators=[Optional()])
  submit    = SubmitField('Breyta')


