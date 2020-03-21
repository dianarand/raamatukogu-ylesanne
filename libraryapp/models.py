from datetime import date, timedelta
from libraryapp import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.Date, default=date.today, nullable=False)
    location = db.Column(db.Integer, nullable=False)
    #time_limit = db.Column(db.Integer, default=4, nullable=False)
    lender_id = db.Column(db.Integer, db.ForeignKey('lender.id'))
    #deadline = db.Column(db.Date, default=(date.today() + timedelta(weeks=self.time_limit)))

    def __repr__(self):
        return f'{self.title} ({self.author})'


class Lender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    lended_books = db.relationship('Book', backref='lender')

    def __repr__(self):
        return f'{self.surname}, {self.name}'
