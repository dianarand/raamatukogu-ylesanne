from flask import redirect, url_for, render_template, request, flash
from libraryapp import app, db
from libraryapp.forms import LoginForm, BookForm, AddLenderForm
from libraryapp.models import Book, Lender, User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Juba sisse logitud!')
        return redirect(url_for('home'))
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
                    return redirect(url_for('home'))
            else:
                flash('Kasutajat ei ole olemas! Proovi uuesti.')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Välja logitud!')
    return redirect(url_for('home'))


@app.route('/status')
def status():
    books = Book.query.all()
    return render_template('status.html', books=books)


@app.route('/book/new', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.admin:
        form = BookForm()
        if form.validate_on_submit():
            title = form.title.data
            author = form.author.data
            location = form.location.data
            book = Book(title=title, author=author, location=location)
            db.session.add(book)
            db.session.commit()
            flash('Raamat lisatud!')
            return redirect(url_for('home'))
        return render_template('add_book.html', form=form)
    else:
        flash('Puuduvad õigused')
        return redirect(url_for('home'))


@app.route('/add_lender', methods=['GET', 'POST'])
@login_required
def add_lender():
    form = AddLenderForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        lender = Lender(name=name, surname=surname)
        db.session.add(lender)
        db.session.commit()
        flash('Laenutaja lisatud!')
        return redirect(url_for('home'))
    return render_template('add_lender.html', form=form)
