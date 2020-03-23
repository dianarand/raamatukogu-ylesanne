from datetime import date, datetime, timedelta
from flask import Blueprint, redirect, url_for, render_template, request, flash, make_response, jsonify, current_app
from flask_login import login_user, current_user, logout_user, login_required
from libraryapp.models import Book, User
from libraryapp.main.forms import LoginForm
import jwt
from werkzeug.security import check_password_hash
from functools import wraps





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
