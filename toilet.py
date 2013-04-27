from flask import Flask

from db import db
from api.views import api
from toilet.views import toilet

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)

# API
app.register_blueprint(api, url_prefix='/api')

# Web
app.register_blueprint(toilet)

# Debug
@app.route('/install')
def install():
    db.drop_all()
    db.create_all()

    # Sample data
    from toilet.models import Category, Tag, Toilet

    cat_public = Category('public')
    db.session.add(cat_public)
    cat_commercial = Category('commercial')
    db.session.add(cat_commercial)
    cat_paid = Category('paid')
    db.session.add(cat_paid)
    cat_code = Category('code')
    db.session.add(cat_code)

    tag_disabled = Tag('disabled')
    db.session.add(tag_disabled)

    t_sihlpost = Toilet('Sihlpost', 47.375312, 8.532493)
    t_sihlpost.category = cat_commercial
    t_sihlpost.tags.append(tag_disabled)
    db.session.add(t_sihlpost)
    db.session.commit()

    return 'Installed'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
