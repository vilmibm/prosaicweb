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

from flask import render_template, request
# TODO don't use DEFAULT_DB
from ..models import Corpus, get_session, DEFAULT_DB

# TODO types?

def index():
    return "main page lulz"

def corpora(): 
    # TODO block on auth
    if request.method == 'GET':
        context = {'corpora':[],
                   # 'authenticated': False, }
                   'authenticated': True,
                   'username': 'vilmibm'}
        return render_template('corpora.html', **context)

    if request.method == 'POST':
        return "TODO"

    if request.method == 'PUT':
        return "TODO"

    if request.method == 'DELETE':
        return "TODO"

def sources(): pass
def templates(): pass
def generate(): pass
