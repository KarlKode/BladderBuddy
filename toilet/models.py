from db import db


tags = db.Table('tags',
                db.Column('toilet_id', db.Integer, db.ForeignKey('toilet.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Toilet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    latitude = db.Column(db.Float(precision=64))
    longitude = db.Column(db.Float(precision=64))
    address = db.Column(db.Text)
    description = db.Column(db.Text)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('toilets', lazy='dynamic'))
    features = db.relationship('Feature', secondary=tags, backref=db.backref('toilets', lazy='dynamic'))

    def __init__(self, title, latitude, longitude):
        self.title = title
        self.latitude = latitude
        self.longitude = longitude

    def __json__(self):
        return {
            'title': self.title,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'description': self.description,
            'category': self.category.title,
            'features': [f.title for f in self.features]
        }

    def __repr__(self):
        return '<Toilet %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Category %r>' % self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Tag %r>' % self.title
