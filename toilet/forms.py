from flask.ext.wtf import Form, TextField, FloatField, HiddenInput, TextAreaField


class ToiletAddForm(Form):
    title = TextField('title')
    latitude = FloatField('latitude')
    longitude = FloatField('longitude')


class ToiletSearchForm(Form):
    latitude = FloatField('latitude')
    longitude = FloatField('longitude')
