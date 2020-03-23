from datetime import date
from flask import Blueprint, redirect, url_for, render_template, flash, jsonify
from flask_login import login_required
from libraryapp import db
from libraryapp.models import Lender
from libraryapp.lenders.forms import AddForm, SearchForm

lenders = Blueprint('lenders', __name__)


@lenders.route('/lender', methods=['POST'])
def create_lender():
    data = request.get_json()
    new_lender = Lender(name=data['name'], surname=data['surname'], personal_code=['personal_code'])
    db.session.add(new_lender)
    db.session.commit()
    return jsonify({'message': 'Laenutaja lisatud!'})


@lenders.route('/lender/<int:lender_id>', methods=['GET'])
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

# @lenders.route('/lender/search', methods=['GET', 'POST'])
# @login_required
# def lender_search():
#     form = SearchForm()
#     if form.validate_on_submit():
#         if form.surname.data and form.code.data:
#             result = Lender.query.filter_by(surname=form.surname.data, personal_code=form.code.data).all()
#         elif form.surname.data:
#             result = Lender.query.filter_by(surname=form.surname.data).all()
#         elif form.code.data:
#             result = Lender.query.filter_by(personal_code=form.code.data).all()
#         else:
#             flash('Sisesta info')
#             return render_template('search.html', title='Laenutaja otsing', form=form)
#         return render_template('lender_result.html', result=result)
#     return render_template('search.html', title='Laenutaja otsing', form=form)
