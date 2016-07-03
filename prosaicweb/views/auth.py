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

from flask import request, redirect, render_template
from flask_login import login_user, logout_user, login_required

from ..app import bcrypt
from ..models import User, get_session, DEFAULT_DB
from ..util import get_method

@login_required
def account():
    method = get_method(request)
    return 'lol'

@login_required
def logout():
    logout_user()
    return redirect('/')

def login():
    if request.method == 'POST':
        session = get_session(DEFAULT_DB)
        email = request.form['email']
        password = request.form['password']

        user = session.query(User).filter(User.email == email).one()
        pwhash = bytes(user.pwhash, 'utf-8')

        if not bcrypt.check_password_hash(pwhash, password):
            return redirect('/auth/login')

        login_user(user, remember=True)

        return redirect('/generate')

def register():
    if request.method == 'GET':
        return render_template('/register.html')

    if request.method == 'POST':
        session = get_session(DEFAULT_DB)
        email = request.form['email']
        password = request.form['password']
        pwhash = bcrypt.generate_password_hash(password).decode()
        user = User(email=email, pwhash=pwhash)

        session.add(user)
        session.commit()

        login_user(user, remember=True)

        return redirect('/generate')
