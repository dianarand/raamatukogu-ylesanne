from typing import Dict, List, Any

import jwt
import logging
from functools import wraps
from datetime import date, datetime, timedelta
from flask import current_app, request, jsonify, abort
from werkzeug.security import check_password_hash
from libraryapp import db, app
from libraryapp.models import User, Book, Lender

logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


def log_info(current_user, message):
    """Logs message into log file with username"""
    logger.info(f'{current_user.username} : {message}')


def token_required(f):
    """Checks user for valid token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            logger.info('Token not found')
            abort(401)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.get(data['id'])
        except:
            logger.info('Token not valid')
            abort(401)
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/login', methods=['GET'])
def login():
    """Login route"""
    logger.info('Attempting to log in')
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        logger.info('FAIL : Cannot verify user')
        abort(401)
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        logger.info('FAIL : Username {auth.username} not found')
        abort(401)
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           current_app.config['SECRET_KEY'])
        logger.info('SUCCESS')
        return jsonify({'token': token.decode('UTF-8')})
    logger.info('FAIL : Password incorrect for user {user.username}')
    abort(401)


@app.route('/book', methods=['GET'])
def get_available_books():
    """Returns dictionary of currently available books"""
    logger.info('Getting available books')
    available_books = Book.query.filter_by(lender_id=None).all()
    no_duplicates = []
    for curr_book in available_books:
        tba = Book.query.filter_by(
            title=curr_book.title,
            author=curr_book.author,
            lender_id=None
        ).first()
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
    logger.info('SUCCESS')
    return jsonify({'available_books': output})


@app.route('/overtime', methods=['GET'])
@token_required
def get_overtime_lenders(current_user):
    """Returns dictionary of lenders with overtime books"""
    log_info(current_user, 'Getting overtime lenders')
    if not current_user.employee:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    lended_books = Book.query.filter(Book.deadline != None)
    overtime_books = []
    for curr_book in lended_books:
        if curr_book.deadline < date.today():
            overtime_books.append(curr_book)
    output = []
    for curr_book in overtime_books:
        book_data = {
            'lender': curr_book.lender.name + ' ' + curr_book.lender.surname,
            'title': curr_book.title,
            'overtime': curr_book.overtime()
        }
        output.append(book_data)
    log_info(current_user, 'SUCCESS')
    return jsonify({'overtime_books': output})


@app.route('/book', methods=['POST'])
@token_required
def create_book(current_user):
    """Adds a new book"""
    log_info(current_user, 'Creating new book')
    if not current_user.admin:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], location=data['location'])
    db.session.add(new_book)
    db.session.commit()
    log_info(current_user, 'SUCCESS')
    return jsonify({'message': 'Raamat lisatud!'})


@app.route('/book/<int:book_id>', methods=['GET'])
@token_required
def get_book(current_user, book_id):
    """Returns dictionary with information about a book with a given ID"""
    log_info(current_user, 'Getting book information')
    if not current_user.employee:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    curr_book = Book.query.get(book_id)
    if not curr_book:
        log_info(current_user, 'FAIL : Book not found')
        abort(404)
    book_data = {
        'title': curr_book.title,
        'author': curr_book.author,
        'availability': curr_book.availability(),
        'time_limit': curr_book.time_limit(),
        'location': curr_book.location
    }
    if curr_book.lender_id:
        curr_lender = Lender.query.get(curr_book.lender_id)
        book_data.update({
            'lender_id': curr_book.lender_id,
            'lender': curr_lender.name + ' ' + curr_lender.surname,
            'deadline': curr_book.deadline
        })
    log_info(current_user, 'SUCCESS')
    return jsonify({'book': book_data})


@app.route('/book/<int:book_id>', methods=['POST'])
@token_required
def checkin_book(current_user, book_id):
    """Checks in book with a given ID, assuming it has been checked out"""
    log_info(current_user, 'Checking book in')
    if not current_user.employee:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    curr_book = Book.query.get(book_id)
    if not curr_book:
        log_info(current_user, 'FAIL : Book not found')
        abort(404)
    if not curr_book.lender_id:
        log_info(current_user, 'FAIL : Book not checked out')
        abort(400)
    curr_book.checkin()
    db.session.commit()
    log_info(current_user, 'SUCCESS')
    return jsonify({'message': 'Raamat on tagastatud!'})


@app.route('/book/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user, book_id):
    """Deletes book with a given ID"""
    log_info(current_user, 'Deleting book')
    if not current_user.admin:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    curr_book = Book.query.get(book_id)
    if not curr_book:
        log_info(current_user, 'FAIL : Book not found')
        abort(404)
    db.session.delete(curr_book)
    db.session.commit()
    log_info(current_user, 'SUCCESS')
    return jsonify({'message': 'Raamat on kustutatud!'})


@app.route('/book/<int:book_id>/<int:lender_id>/<int:weeks>', methods=['POST'])
@app.route('/book/<int:book_id>/<int:lender_id>', methods=['POST'], defaults={'weeks': None})
@token_required
def checkout_book(current_user, book_id, lender_id, weeks):
    """Checks out book with a given ID to a lender with a given ID"""
    log_info(current_user, 'Checking book out')
    if not current_user.employee:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    curr_book = Book.query.get(book_id)
    if not curr_book:
        log_info(current_user, 'FAIL : Book not found')
        abort(404)
    curr_lender = Lender.query.get(lender_id)
    if not curr_lender:
        log_info(current_user, 'FAIL : Lender not found')
        abort(404)
    curr_book.checkout(lender_id, weeks)
    db.session.commit()
    log_info(current_user, 'SUCCESS')
    return jsonify({'message': 'Raamat on välja laenutatud!'})


@app.route('/book/search', methods=['POST'])
@token_required
def book_search(current_user):
    """Searches for a book by given title or author or both"""
    log_info(current_user, 'Searching for books')
    if not current_user.employee:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    data = request.get_json()
    if 'title' in data and 'author' in data:
        book_list = Book.query.filter_by(title=data['title'], author=data['author']).all()
    elif 'title' in data:
        book_list = Book.query.filter_by(title=data['title']).all()
    elif 'author' in data:
        book_list = Book.query.filter_by(author=data['author']).all()
    else:
        log_info(current_user, 'FAIL : Bad request')
        abort(400)
    output = []
    for curr_book in book_list:
        book_data = {
            'book_id': curr_book.id,
            'title': curr_book.title,
            'author': curr_book.author,
            'time_limit': curr_book.time_limit(),
            'location': curr_book.location
        }
        if curr_book.lender_id:
            curr_lender = Lender.query.get(curr_book.lender_id)
            book_data.update({
                'lender_id': curr_book.lender_id,
                'lender': curr_lender.name + ' ' + curr_lender.surname,
                'deadline': curr_book.deadline
            })
        output.append(book_data)
    log_info(current_user, 'SUCCESS')
    return jsonify({'books': output})


@app.route('/lender', methods=['POST'])
@token_required
def create_lender(current_user):
    """Adds a new lender"""
    log_info(current_user, 'Creating new lender')
    if not current_user.employee:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    data = request.get_json()
    new_lender = Lender(
        name=data['name'],
        surname=data['surname'],
        personal_code=data['personal_code']
    )
    db.session.add(new_lender)
    db.session.commit()
    log_info(current_user, 'SUCCESS')
    return jsonify({'message': 'Laenutaja lisatud!'})


@app.route('/lender/<int:lender_id>', methods=['GET'])
@token_required
def get_lender(current_user, lender_id):
    """Returns dictionary with information about a lender with a given ID"""
    log_info(current_user, 'Getting lender information')
    if not current_user.employee:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    curr_lender = Lender.query.get(lender_id)
    if not curr_lender:
        log_info(current_user, 'FAIL : Lender not found')
        abort(404)
    lended_books = {
        'titles': [book.title for book in curr_lender.books],
        'deadlines': [book.deadline for book in curr_lender.books]
    }
    lender_data = {
        'name': curr_lender.name,
        'surname': curr_lender.surname,
        'personal_code': curr_lender.personal_code,
        'lended_books': lended_books
    }
    log_info(current_user, 'SUCCESS')
    return jsonify({'lender': lender_data})


@app.route('/lender/search', methods=['POST'])
@token_required
def lender_search(current_user):
    """Searches for a lender by given surname or personal code or both"""
    log_info(current_user, 'Searching for lenders')
    if not current_user.employee:
        log_info(current_user, 'FAIL : Unauthorized')
        abort(403)
    data = request.get_json()
    if 'surname' in data and 'personal_code' in data:
        lender_list = Lender.query.filter_by(
            surname=data['surname'],
            personal_code=data['personal_code']
        ).all()
    elif 'surname' in data:
        lender_list = Lender.query.filter_by(surname=data['surname']).all()
    elif 'personal_code' in data:
        lender_list = Lender.query.filter_by(personal_code=data['personal_code']).all()
    else:
        log_info(current_user, 'FAIL : Bad request')
        abort(400)
    output = []
    for curr_lender in lender_list:
        lender_data = {
            'lender_id': curr_lender.id,
            'name': curr_lender.name,
            'surname': curr_lender.surname,
            'personal_code': curr_lender.personal_code,
            'lended_books': [book.title for book in curr_lender.books]
        }
        output.append(lender_data)
    log_info(current_user, 'SUCCESS')
    return jsonify({'lender': output})
