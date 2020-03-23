from datetime import date, datetime, timedelta
from flask import Blueprint, redirect, url_for, render_template, request, flash, make_response, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from libraryapp.models import Book, User
from libraryapp.main.forms import LoginForm
import jwt

main = Blueprint('main', __name__)


@main.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username:
        return make_response('Could not verify', 401)
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify', 401)
    token = jwt.encode({'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')})


@main.route('/overtime', methods=['GET'])
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

# @main.route('/')
# def home():
#     return render_template('home.html')
#
#
# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         flash('Juba sisse logitud!')
#         return redirect(url_for('main.home'))
#     else:
#         form = LoginForm()
#         if form.validate_on_submit():
#             user = User.query.filter_by(username=form.username.data).first()
#             if user:
#                 login_user(user)
#                 next_page = request.args.get('next')
#                 flash('Sisse logitud!')
#                 if next_page:
#                     return redirect(next_page)
#                 else:
#                     return redirect(url_for('main.home'))
#             else:
#                 flash('Kasutajat ei ole olemas! Proovi uuesti.')
#     return render_template('login.html', form=form)
#
#
# @main.route('/logout')
# def logout():
#     if current_user.is_authenticated:
#         logout_user()
#         flash('Välja logitud!')
#     return redirect(url_for('main.home'))
