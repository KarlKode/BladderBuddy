from flask import Blueprint, request, jsonify, abort

from toilet.models import Toilet

api = Blueprint('toilet_api', __name__)

@api.route('/')
def index():
    return 'Toilet hello world'


@api.route('/nearby')
def nearby():
    try:
        latitude = float(request.args.get('lat'))
        longitude = float(request.args.get('long'))
    except (ValueError, TypeError):
        raise abort(404)
    toilets = Toilet.query.filter(
        Toilet.latitude > latitude - 1,
        Toilet.latitude < latitude + 1,
        Toilet.longitude > longitude - 1,
        Toilet.longitude < longitude + 1)
    return jsonify(toilets=[t.__json__() for t in toilets])