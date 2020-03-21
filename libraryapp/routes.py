from flask import redirect, url_for, render_template, request, session, flash
from libraryapp import app
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
        user = request.form['nm']
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
    return render_template('status.html')


@app.route('/add_book')
def add_book():
    if 'user' in session:
        return '<h1>Raamatu lisamine</h1>'
    else:
        flash('Ei ole sisse logitud')
        return redirect(url_for('login'))
