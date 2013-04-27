from flask import Blueprint, request, render_template, redirect, url_for
import json

from db import db
from forms import ToiletAddForm, ToiletSearchForm
from models import Toilet, Category, Tag

toilet = Blueprint('toilet', __name__)


@toilet.route('/')
def index():
    categories_json = json.dumps([category.__json__() for category in Category.query.all()])
    tags_json = json.dumps([tag.__json__() for tag in Tag.query.all()])
    return render_template('index.html', categories_json=categories_json, tags_json=tags_json)


@toilet.route('/<int:toilet_id>')
def show(toilet_id):
    t = Toilet.query.get_or_404(toilet_id)
    return render_template('show_toilet.html', toilet=t)


@toilet.route('/add', methods=['GET', 'POST'])
def add():
    form = ToiletAddForm(request.form)
    if request.method == 'POST' and form.validate():
        t = Toilet(form.title.data, form.latitude.data, form.longitude.data)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('.show', toilet_id=t.id))
    return render_template('add_toilet.html', toilet_form=form)


@toilet.route('/search', methods=['GET', 'POST'])
def search():
    form = ToiletSearchForm(request.form)
    toilets = []
    if request.method == 'POST' and form.validate():
        toilets = Toilet.search(form.latitude.data, form.longitude.data)
    return render_template('search_toilets.html', search_form=form, toilets=toilets)