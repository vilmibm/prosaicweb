# prosaicweb
# Copyright (C) 2016  nathaniel smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required

from ..app import bcrypt, app
from ..models import User, get_session
from ..util import get_method, ResponseData

BAD_CREDS_MSG = 'no such user or bad password'

@login_required
def logout() -> ResponseData:
    logout_user()
    return redirect(url_for('index'))

def login() -> ResponseData:
    if request.method == 'POST':
        session = get_session(app.config['DB'])
        email = request.form['email']
        password = request.form['password']

        user = session.query(User).filter(User.email == email).one_or_none()
        if user is None:
            flash(BAD_CREDS_MSG)
            return redirect(url_for('register'))
        pwhash = bytes(user.pwhash, 'utf-8')

        if not bcrypt.check_password_hash(pwhash, password):
            flash(BAD_CREDS_MSG)
            return redirect(url_for('register'))

        login_user(user, remember=True)

        return redirect(url_for('generate'))

def register() -> ResponseData:
    if request.method == 'GET':
        return render_template('/register.html')

    if request.method == 'POST':
        session = get_session(app.config['DB'])
        email = request.form['email']
        password = request.form['password']
        pwhash = bcrypt.generate_password_hash(password).decode()
        user = User(email=email, pwhash=pwhash)

        session.add(user)
        session.commit()

        login_user(user, remember=True)

        return redirect(url_for('generate'))
