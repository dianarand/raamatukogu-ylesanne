from flask import Blueprint, redirect, url_for, render_template, flash, abort, request, jsonify
from flask_login import current_user, login_required
from libraryapp import db
from libraryapp.models import Book, Lender
from libraryapp.books.forms import AddForm, LendForm, SearchForm, ConfirmButton

books = Blueprint('books', __name__)


@books.route('/book', methods=['GET'])
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


@books.route('/book', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], location=data['location'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Raamat lisatud!'})


@books.route('/book/<int:book_id>', methods=['GET'])
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


@books.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    curr_book = Book.query.get(book_id)
    if not curr_book:
        return jsonify({'message': 'Pole sellist raamatut!'})
    db.session.delete(curr_book)
    db.session.commit()
    return jsonify({'message': 'Raamat on kustutatud!'})


# @books.route('/book/search', methods=['GET', 'POST'])
# @login_required
# def book_search():
#     form = SearchForm()
#     if form.validate_on_submit():
#         if form.title.data and form.author.data:
#             result = Book.query.filter_by(title=form.title.data, author=form.author.data).all()
#         elif form.title.data:
#             result = Book.query.filter_by(title=form.title.data).all()
#         elif form.author.data:
#             result = Book.query.filter_by(author=form.author.data).all()
#         else:
#             flash('Sisesta info')
#             return render_template('search.html', title='Raamatu otsing', form=form)
#         return render_template('book_result.html', result=result)
#     return render_template('search.html', title='Raamatu otsing', form=form)
#
#
# @books.route('/book/<int:book_id>/lend', methods=['GET', 'POST'])
# @login_required
# def lend_book(book_id):
#     book = Book.query.get_or_404(book_id)
#     form = LendForm()
#     # form.time_limit.data = book.time_limit()
#     if form.validate_on_submit():
#         lender = Lender.query.filter_by(personal_code=form.code.data).first()
#         if lender:
#             book.checkout(lender_id=lender.id)
#             db.session.commit()
#             flash(f'Raamat on laenutatud kasutajale {lender}')
#             return redirect(url_for('main.home'))
#         else:
#             flash('Laenutajat ei ole olemas! Proovi uuesti.')
#     return render_template('add_lender.html', title='Raamatu laenutamine', book=book, form=form)
#
#
# @books.route('/book/<int:book_id>/return', methods=['GET', 'POST'])
# @login_required
# def return_book(book_id):
#     book = Book.query.get_or_404(book_id)
#     lender = Lender.query.get(book.lender_id)
#     form = ConfirmButton()
#     if form.validate_on_submit():
#         book.checkin()
#         db.session.commit()
#         flash(f'Raamat "{book.title}" on tagastatud kasutajalt {lender}')
#         return redirect(url_for('main.home'))
#     return render_template('add_lender.html', title='Raamatu tagastamine', book=book, lender=lender, form=form)
