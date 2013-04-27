from db import db


tags = db.Table('tags',
                db.Column('toilet_id', db.Integer, db.ForeignKey('toilet.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Toilet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    lat = db.Column(db.Float(precision=64))
    lng = db.Column(db.Float(precision=64))
    address = db.Column(db.Text)
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    code = db.Column(db.String(10))
    time_open = db.Column(db.Time)
    time_close = db.Column(db.Time)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('toilets', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('toilets', lazy='dynamic'))

    @staticmethod
    def search(latitude, longitude):
        query = Toilet.query
        latitude_min = latitude - 0.25
        latitude_max = latitude + 0.25
        if latitude_min < -90:
            latitude_min += 180
            query = query.filter(db.or_(Toilet.lat >= latitude_min, Toilet.lat <= latitude_max))
        elif latitude_max > 90:
            latitude_max -= 180
            query = query.filter(db.or_(Toilet.lat >= latitude_min, Toilet.lat <= latitude_max))
        else:
            query = query.filter(Toilet.lat >= latitude_min, Toilet.lat <= latitude_max)
        longitude_min = longitude - 0.5
        longitude_max = longitude + 0.5
        if longitude_min < -180:
            longitude_min += 360
            query = query.filter(db.or_(Toilet.lng >= longitude_min, Toilet.lng <= longitude_max))
        elif longitude_max > 180:
            longitude_max -= 360
            query = query.filter(db.or_(Toilet.lng >= longitude_min, Toilet.lng <= longitude_max))
        else:
            query = query.filter(Toilet.lng >= longitude_min, Toilet.lng <= longitude_max)
        return query

    def __init__(self, title, lat, lng):
        self.title = title
        self.lat = lat
        self.lng = lng

    def __json__(self):
        category = 'Unknown'
        if self.category:
            category = self.category.__json__()
        tags = []
        return {
            'id': self.id,
            'title': self.title,
            'lat': self.lat,
            'lng': self.lng,
            'address': self.address,
            'description': self.description,
            'price': self.price,
            'code': self.code,
            'category': category,
            'tags': [tag.__json__() for tag in self.tags]
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


    def __json__(self):
        return {'id': self.id, 'title': self.title}


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Tag %r>' % self.title


    def __json__(self):
        return {'id': self.id, 'title': self.title}
