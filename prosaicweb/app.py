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
from typing import Optional

from flask import Flask, redirect, url_for, flash
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from .cfg import DEBUG, SECRET_KEY, MAX_UPLOAD_SIZE, DB
from .models import User, get_session, Database
from .util import ResponseData

app = Flask('prosaicweb')
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

app.config['DEBUG'] = DEBUG
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE
app.config['DB'] = Database(**DB)

@login_manager.unauthorized_handler
def unauthorized() -> ResponseData:
    flash('please login to do stuff.')
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(email: str) -> Optional[User]:
    session = get_session(app.config['DB'])
    users = session.query(User).filter(User.email == email).all()

    if len(users) == 0:
        return None

    if len(users)  > 1:
        return None

    return users[0]
