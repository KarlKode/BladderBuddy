from flask import Blueprint, request, render_template, redirect, url_for

from db import db
from forms import ToiletForm
from models import Toilet

toilet = Blueprint('toilet', __name__)


@toilet.route('/')
def index():
    return render_template('index.html')


@toilet.route('/<int:toilet_id>')
def show(toilet_id):
    t = Toilet.query.get_or_404(toilet_id)
    return render_template('show_toilet.html', toilet=t)


@toilet.route('/add', methods=['GET', 'POST'])
def add():
    form = ToiletForm(request.form)
    if request.method == 'POST' and form.validate():
        t = Toilet(form.title.data, form.latitude.data, form.longitude.data)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('.show', toilet_id=t.id))
    return render_template('add_toilet.html', toilet_form=form)

