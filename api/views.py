from flask import Blueprint, request, jsonify, abort

from db import db
from toilet.models import Toilet

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return 'Toilet hello world'


@api.route('/toilets', methods=['GET'])
def toilets():
    if request.method == 'GET':
        try:
            lat = float(request.args.get('lat'))
            lng = float(request.args.get('lng'))
        except (ValueError, TypeError):
            raise abort(404)
        toilets = Toilet.search(lat, lng).all()
        return jsonify(toilets=[t.__json__() for t in toilets])


@api.route('/toilet', methods=['GET', 'PUT'])
def toilet():
    if request.method == 'GET':
        try:
            id = int(request.args.get('id'))
        except (ValueError, TypeError):
            raise abort(404)
        t = Toilet.query.get_or_404(id)
        return jsonify(toilet=t.__json__())
    if request.method == 'PUT':
        try:
            title = request.form.get('title')
            if not title:
                raise ValueError('Invalid title')
            description = request.form.get('description')
            address = request.form.get('address')
            category_id = int(request.form.get('category'))
            lat = float(request.form.get('lat'))
            lng = float(request.form.get('lng'))
            price = int(request.form.get('price'))
            code = request.form.get('code')
            time_open = request.form.get('time_open')
            time_close = request.form.get('time_close')
            t = Toilet(title, lat, lng)
            t.description = description
            t.address = address
            t.category_id = category_id
            t.price = price
            t.code = code
            print request.form
            print time_open
            #t.time_open = time_open
            #t.time_close = time_close
            db.session.add(t)
            db.session.commit()
            return jsonify(success='success')
        except:
            raise abort(500)
