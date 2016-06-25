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

from flask import render_template, request, redirect
# TODO don't use DEFAULT_DB
from ..models import Source, Corpus, get_session, DEFAULT_DB

# TODO types?

def index():
    return "main page lulz"

class Foo:
    def __init__(self, x, y):
        self.name = x
        self.description = y

def corpora(): 
    # TODO block on auth
    if request.method == 'GET':
        session = get_session(DEFAULT_DB)
        corpora = session.query(Corpus).all()
        context = {'corpora': corpora,
                   'authenticated': True,
                   'username': 'vilmibm'}
        return render_template('corpora.html', **context)

def sources():
    # TODO block on auth
    if request.method == 'GET':
        session = get_session(DEFAULT_DB)
        sources = session.query(Source).all()
        for source in sources:
            source.content_preview = source.content[0:250] + '...'
        context = {'sources':sources,
                   'authenticated':True,
                   'username': 'vilmibm'}
        return render_template('sources.html', **context)

def source(source_id):
    if request.method == 'GET':
        session = get_session(DEFAULT_DB)
        s = session.query(Source).filter(Source.id == source_id).one()
        context = {
            'source':s,
            'authenticated':True,
            'username':'vilmibm',
        }
        return render_template('source.html', **context)

    # srsly not rest at all. this is an update
    if request.method == 'POST':
        session = get_session(DEFAULT_DB)
        s = session.query(Source).filter(Source.id == source_id).one()
        s.name = request.form['source_name']
        s.description = request.form['source_description']
        # TODO check if different and regenerate all phrases if so
        s.content = request.form['source_content']
        session.commit()
        return redirect('/sources')

def templates(): pass
def generate(): pass
