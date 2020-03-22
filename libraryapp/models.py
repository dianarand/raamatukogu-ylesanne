from datetime import date, timedelta
from libraryapp import db, login_manager
from flask_login import UserMixin


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    location = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.Date, default=date.today, nullable=False)
    lender_id = db.Column(db.Integer, db.ForeignKey('lender.id'))
    deadline = db.Column(db.Date)

    def __repr__(self):
        return f'{self.title} ({self.author})'

    def availability(self):
        return len(Book.query.filter_by(title=self.title, author=self.author).all())

    def time_limit(self, custom=None):
        if custom:
            return custom
        else:
            #if (date.today - self.date_added).months < 3:
            #    return 1
            if self.availability() < 5:
                return 1
            else:
                return 4

    def checkout(self, lender_id, limit=None):
        self.lender_id = lender_id
        self.deadline = date.today() + timedelta(weeks=self.time_limit(limit))

    def checkin(self):
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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
