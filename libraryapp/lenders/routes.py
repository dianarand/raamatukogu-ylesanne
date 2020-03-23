from datetime import date
from flask import Blueprint, redirect, url_for, render_template, flash, request, jsonify
from flask_login import login_required
from libraryapp import db
from libraryapp.models import Lender
from libraryapp.lenders.forms import AddForm, SearchForm


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
