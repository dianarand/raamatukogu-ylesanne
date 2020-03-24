from datetime import date, timedelta
from libraryapp import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    location = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.Date, default=date.today(), nullable=False)
    lender_id = db.Column(db.Integer, db.ForeignKey('lender.id'))
    deadline = db.Column(db.Date)

    def __repr__(self):
        return f'{self.title} ({self.author})'

    def availability(self):
        """Returns number of books available with same title and author"""
        return len(Book.query.filter_by(title=self.title, author=self.author, lender_id=None).all())

    def locations(self):
        """Returns all locations for books with same title and author"""
        books = Book.query.filter_by(title=self.title, author=self.author, lender_id=None).all()
        locations = []
        for book in books:
            if book.location not in locations:
                locations.append(book.location)
        locations.sort()
        return locations

    def time_limit(self):
        """Returns time limit in weeks for lending given book"""
        if (date.today() - self.date_added).days / 30 < 3:
            return 1
        if self.availability() < 5:
            return 1
        return 4

    def overtime(self):
        """Returns number of overtime days if book has been not returned before deadline"""
        days = (date.today() - self.deadline).days
        if days > 0:
            return days
        return None

    def checkout(self, lender_id, weeks):
        """Checks out book to a lender with given ID"""
        if weeks:
            self.deadline = date.today() + timedelta(weeks=weeks)
        else:
            self.deadline = date.today() + timedelta(weeks=self.time_limit())
        self.lender_id = lender_id

    def checkin(self):
        """Checks book in to library"""
        self.lender_id = None
        self.deadline = None


class Lender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    personal_code = db.Column(db.String(11), nullable=False)
    books = db.relationship('Book', backref='lender')

    def __repr__(self):
        return f'{self.name} {self.surname}'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    employee = db.Column(db.Boolean, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
