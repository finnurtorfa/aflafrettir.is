from flask.ext.wtf import Form

from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required, Length, Email 

class ContactForm(Form):
  name    = TextField('Nafn', validators=[Required(), Length(1,64)])
  email   = TextField('E-mail', validators=[Required(), Email()])
  subject = TextField('Efni', validators=[Required()])
  message = TextAreaField('Skilaboð', validators=[Required()])
  submit  = SubmitField('Senda')
