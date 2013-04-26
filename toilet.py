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
    db.create_all()

    # Sample data
    from toilet.models import Category, Toilet

    c1 = Category('public')
    c2 = Category('paid')
    db.session.add(c1)
    db.session.add(c2)
    t1 = Toilet('test', 47.375312, 8.532493)
    t1.category = c1
    db.session.add(t1)
    db.session.commit()

    return 'Installed'

if __name__ == '__main__':
    app.run(debug=True)