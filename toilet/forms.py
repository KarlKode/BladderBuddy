from flask.ext.wtf import Form, TextField, DecimalField


class ToiletForm(Form):
    title = TextField('title')
    latitude = DecimalField('latitude')
    longitude = DecimalField('longitude')
