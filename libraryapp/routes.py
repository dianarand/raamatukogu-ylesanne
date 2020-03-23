import jwt
from libraryapp import db, app
from libraryapp.models import User, Book, Lender
from flask import make_response, current_app, request, jsonify
from datetime import date, datetime, timedelta
from werkzeug.security import check_password_hash


@app.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Sisselogimine ei õnnestunud')
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Sisselogimine ei õnnestunud')
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           current_app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Sisselogimine ei õnnestunud')


@app.route('/overtime', methods=['GET'])
def get_overtime_lenders():
    lended_books = Book.query.filter(Book.deadline != None)
    overtime_books = []
    for curr_book in lended_books:
        if curr_book.deadline < date.today():
            overtime_books.append(curr_book)
    output = []
    for curr_book in overtime_books:
        data = {
            'lender': curr_book.lender.name + ' ' + curr_book.lender.surname,
            'title': curr_book.title,
            'overtime': curr_book.overtime()
        }
        output.append(data)
    return jsonify({'overtime': output})

@app.route('/book', methods=['GET'])
def get_available_books():
    available_books = Book.query.filter_by(lender_id=None).all()
    no_duplicates = []
    for curr_book in available_books:
        tba = Book.query.filter_by(title=curr_book.title, author=curr_book.author, lender_id=None).first()
        if tba not in no_duplicates:
            no_duplicates.append(tba)
    output = []
    for curr_book in no_duplicates:
        book_data = {
            'title': curr_book.title,
            'author': curr_book.author,
            'availability': curr_book.availability(),
            'time_limit': curr_book.time_limit(),
            'location': curr_book.locations()
        }
        output.append(book_data)
    return jsonify({'available_books': output})


@app.route('/book', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], location=data['location'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Raamat lisatud!'})


@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    curr_book = Book.query.get(book_id)
    if not curr_book:
        return jsonify({'message': 'Pole sellist raamatut!'})
    data = {
        'title': curr_book.title,
        'author': curr_book.author,
        'availability': curr_book.availability(),
        'time_limit': curr_book.time_limit(),
        'location': curr_book.location
    }
    return jsonify({'book': data})


@app.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    curr_book = Book.query.get(book_id)
    if not curr_book:
        return jsonify({'message': 'Pole sellist raamatut!'})
    db.session.delete(curr_book)
    db.session.commit()
    return jsonify({'message': 'Raamat on kustutatud!'})

@app.route('/lender', methods=['POST'])
def create_lender():
    data = request.get_json()
    new_lender = Lender(name=data['name'], surname=data['surname'], personal_code=data['personal_code'])
    db.session.add(new_lender)
    db.session.commit()
    return jsonify({'message': 'Laenutaja lisatud!'})


@app.route('/lender/<int:lender_id>', methods=['GET'])
def get_lender(lender_id):
    curr_lender = Lender.query.get(lender_id)
    if not curr_lender:
        return jsonify({'message': 'Pole sellist laenutajat!'})
    data = {
        'name': curr_lender.name,
        'surname': curr_lender.surname,
        'personal_code': curr_lender.personal_code,
        'lended_books': [book.title for book in curr_lender.books]
    }
    return jsonify({'lender': data})

