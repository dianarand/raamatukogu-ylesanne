from flask import redirect, url_for, render_template, request, session, flash
from libraryapp import app, db
from libraryapp.forms import LoginForm, AddBookForm, AddLenderForm
from libraryapp.models import Book, Lender, User
from flask_login import login_user, current_user, logout_user


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
                flash('Sisse logitud!')
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


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'user' in session:
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            location = request.form['location']
            book = Book(title=title, author=author, location=location)
            db.session.add(book)
            db.session.commit()
            flash('Raamat lisatud!')
            return redirect(url_for('home'))
        else:
            form = AddBookForm()
            return render_template('add_book.html', form=form)
    else:
        flash('Ei ole sisse logitud')
        return redirect(url_for('login'))


@app.route('/add_lender', methods=['GET', 'POST'])
def add_lender():
    if 'user' in session:
        if request.method == 'POST':
            name = request.form['name']
            surname = request.form['surname']
            lender = Lender(name=name, surname=surname)
            db.session.add(lender)
            db.session.commit()
            flash('Laenutaja lisatud!')
            return redirect(url_for('home'))
        else:
            form = AddLenderForm()
            return render_template('add_lender.html', form=form)
    else:
        flash('Ei ole sisse logitud')
        return redirect(url_for('login'))
