from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)
app.secret_key = 'mauki'


@app.route('/')
def home():
    if 'user' in session:
        return render_template('user.html')
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
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash('Välja logitud!')
    return redirect(url_for('home'))


@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        return redirect('home')
    else:
        flash('Ei ole sisse logitud')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
