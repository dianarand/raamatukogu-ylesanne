from flask import redirect, url_for, render_template, request, session, flash
from libraryapp import app, db
from libraryapp.models import Book, Lender


@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    else:
        return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        session['user'] = user
        flash('Sisse logitud!')
        return redirect(url_for('home'))
    else:
        if 'user' in session:
            flash('Juba sisse logitud!')
            return redirect(url_for('home'))
        return render_template('login.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
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
            return render_template('add_book.html')
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
            return render_template('add_lender.html')
    else:
        flash('Ei ole sisse logitud')
        return redirect(url_for('login'))
