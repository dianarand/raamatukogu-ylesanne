from datetime import datetime
from libraryapp import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    #release_date = db.Column()
    #location = db.Column()
    #time_limit = db.Column(db.Integer, default=4)
    lender_id = db.Column(db.Integer, db.ForeignKey('lender.id'))
    #deadline = db.Column()

    def __repr__(self):
        return f'{self.title} ({self.author})'


class Lender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    lended_books = db.relationship('Book', backref='lender')

    def __repr__(self):
        return f'{self.surname}, {self.name}'
