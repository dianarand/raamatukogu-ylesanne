from datetime import date
from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from libraryapp.models import Book, User
from libraryapp.main.forms import LoginForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Juba sisse logitud!')
        return redirect(url_for('main.home'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                login_user(user)
                next_page = request.args.get('next')
                flash('Sisse logitud!')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('main.home'))
            else:
                flash('Kasutajat ei ole olemas! Proovi uuesti.')
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Välja logitud!')
    return redirect(url_for('main.home'))


@main.route('/status')
def status():
    available_books = Book.query.filter_by(lender_id=None).all()
    book_list = []
    for book in available_books:
        tba = Book.query.filter_by(title=book.title, author=book.author, lender_id=None).first()
        if tba not in book_list:
            book_list.append(tba)
    return render_template('status.html', books=book_list)


@main.route('/overtime')
@login_required
def overtime():
    lended_books = Book.query.filter(Book.deadline != None)
    overtime_books = []
    for book in lended_books:
        if book.deadline < date.today():
            overtime_books.append(book)
    return render_template('overtime.html', books=overtime_books)
