from app import db

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, index=True, unique=True)
    json = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return '<URL {}>'.format(self.url)    