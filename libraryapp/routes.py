from flask import redirect, url_for, render_template, request, flash, abort
from libraryapp import app, db
from libraryapp.forms import LoginForm, BookForm, LenderForm, BookLendForm, ConfirmButton
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
    if not current_user.admin:
        abort(403)
    else:
        form = BookForm()
        if form.validate_on_submit():
            book = Book(
                title=form.title.data,
                author=form.author.data,
                location=form.location.data
            )
            db.session.add(book)
            db.session.commit()
            flash('Raamat lisatud!')
            return redirect(url_for('home'))
        return render_template('add_book.html', form=form)


@app.route('/book/<int:book_id>')
@login_required
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)


@app.route('/book/<int:book_id>/lend', methods=['GET', 'POST'])
@login_required
def lend_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookLendForm()
    if form.validate_on_submit():
        lender = Lender.query.filter_by(personal_code=form.code.data).first()
        if lender:
            book.lender_id = lender.id
            db.session.commit()
            flash(f'Raamat on laenutatud kasutajale {lender}')
            return redirect(url_for('home'))
        else:
            flash('Laenutajat ei ole olemas! Proovi uuesti.')
    return render_template('lender.html', title='Raamatu laenutamine', book=book, form=form)


@app.route('/book/<int:book_id>/return', methods=['GET', 'POST'])
@login_required
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    lender = Lender.query.get(book.lender_id)
    form = ConfirmButton()
    if form.validate_on_submit():
        book.lender_id = None
        db.session.commit()
        flash(f'Raamat "{book.title}" on tagastatud kasutajalt {lender}')
        return redirect(url_for('home'))
    return render_template('lender.html', title='Raamatu tagastamine', book=book, lender=lender, form=form)


@app.route('/book/<int:book_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    if not current_user.admin:
        abort(403)
    else:
        book = Book.query.get_or_404(book_id)
        form = ConfirmButton()
        if form.validate_on_submit():
            title = book.title
            db.session.delete(book)
            db.session.commit()
            flash(f'Raamat "{title}" on kustutatud')
            return redirect(url_for('home'))
    return render_template('delete.html', book=book, form=form)


@app.route('/add_lender', methods=['GET', 'POST'])
@login_required
def add_lender():
    form = LenderForm()
    if form.validate_on_submit():
        lender = Lender(
            name=form.name.data,
            surname=form.surname.data,
            personal_code=form.code.data
        )
        db.session.add(lender)
        db.session.commit()
        flash('Laenutaja lisatud!')
        return redirect(url_for('home'))
    return render_template('lender.html', title='Lisa uus laenutaja', form=form)
