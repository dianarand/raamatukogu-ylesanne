from flask import Blueprint, redirect, url_for, render_template, flash, abort, request, jsonify
from flask_login import current_user, login_required
from libraryapp import db
from libraryapp.models import Book, Lender
from libraryapp.books.forms import AddForm, LendForm, SearchForm, ConfirmButton


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
