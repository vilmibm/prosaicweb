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
import json

from flask import render_template, request, redirect, Response
from prosaic.parsing import process_text

# TODO don't use DEFAULT_DB
from ..models import Source, Corpus, get_session, DEFAULT_DB, corpora_sources, Phrase, Template

# TODO types?

def get_method(req) -> str:
    return req.form.get('_method', req.method)

def index():
    return "main page lulz"

def corpora():
    method = get_method(request)
    # TODO block on auth
    if method == 'GET':
        session = get_session(DEFAULT_DB)
        context = {'corpora': session.query(Corpus).all(),
                   'sources': session.query(Source).all(),
                   'authenticated': True,
                   'username': 'vilmibm'}
        return render_template('corpora.html', **context)

    if method == 'POST':
        session = get_session(DEFAULT_DB)
        c = Corpus()
        c.name = request.form['corpus_name']
        c.description = request.form['corpus_description']
        for source_id in request.form.getlist('sources'):
            s = session.query(Source).filter(Source.id==source_id).one()
            c.sources.append(s)
        session.add(c)
        session.commit()
        return redirect('corpora/{}'.format(c.id))

def corpus(corpus_id):
    method = get_method(request)

    if method == 'GET':
        session = get_session(DEFAULT_DB)
        c = session.query(Corpus).filter(Corpus.id == corpus_id).one()
        source_ids = map(lambda s: s.id, c.sources)

        other_sources = session.query(Source)\
                        .filter(Source.id.notin_(source_ids))\
                        .all()
        context = {
            'corpus': c,
            'other_sources': other_sources,
            'authenticated':True,
            'username':'vilmibm',
        }
        return render_template('corpus.html', **context)

    if method == 'PUT':
        session = get_session(DEFAULT_DB)
        c = session.query(Corpus).filter(Corpus.id == corpus_id).one()
        c.name = request.form['corpus_name']
        c.description = request.form['corpus_description']
        source_ids = map(int, request.form.getlist('sources'))
        c.sources = session.query(Source).filter(Source.id.in_(source_ids)).all()
        session.commit()

        return redirect('/corpora')

    if method == 'DELETE':
        session = get_session(DEFAULT_DB)
        c = session.query(Corpus).filter(Corpus.id == corpus_id).one()
        c.sources = []
        session.commit()
        session.query(Corpus).filter(Corpus.id == corpus_id).delete()
        session.commit()

        return redirect('/corpora')

def sources():
    method = get_method(request)
    # TODO block on auth
    if method == 'GET':
        session = get_session(DEFAULT_DB)
        sources = session.query(Source).all()
        for source in sources:
            source.content_preview = source.content[0:250] + '...'
        context = {'sources':sources,
                   'authenticated':True,
                   'username': 'vilmibm'}
        return render_template('sources.html', **context)

    if method == 'POST':
        session = get_session(DEFAULT_DB)
        s = Source()
        s.name = request.form['source_name']
        s.description = request.form['source_description']
        content = ''
        if len(request.form['content_paste']) > 0:
            content = request.form['content_paste']
        elif request.files.get('content_file'):
            content = str(request.files['content_file'].read())

        if len(content) == 0:
            return Response('Got empty content for source.', 400)

        session.add(s)
        process_text(s, content)
        session.commit()

        return redirect('/sources/{}'.format(s.id))

def source(source_id):
    method = request.form.get('_method', request.method)

    if method == 'GET':
        session = get_session(DEFAULT_DB)
        s = session.query(Source).filter(Source.id == source_id).one()
        # TODO get this phrase's sources and put em in a table
        context = {
            'source':s,
            'authenticated':True,
            'username':'vilmibm',
        }
        return render_template('source.html', **context)

    if method == 'PUT':
        session = get_session(DEFAULT_DB)
        s = session.query(Source).filter(Source.id == source_id).one()
        s.name = request.form['source_name']
        s.description = request.form['source_description']
        new_content = request.form['source_content']
        if new_content != s.content:
            session.query(Phrase).filter(Phrase.source_id == s.id).delete()
            process_text(s, new_content)
        session.commit()

        return redirect('/sources')

    if method == 'DELETE':
        # TODO for love of god get on delete cascade working
        session = get_session(DEFAULT_DB)
        s = session.query(Source).filter(Source.id==source_id).one()
        corpus_ids = session.query(corpora_sources.c.corpus_id).filter(
            corpora_sources.c.source_id == source_id
        ).all()
        for c in session.query(Corpus).filter(Corpus.id.in_(corpus_ids)):
            c.sources.remove(s)
        session.query(Phrase).filter(Phrase.source_id == source_id).delete()
        session.query(Source).filter(Source.id == source_id).delete()
        session.commit()

        return redirect('/sources')

def phrases():
    # TODO auth
    method = get_method(request)

    if method == 'DELETE':
        session = get_session(DEFAULT_DB)
        s = session.query(Source)\
                   .filter(Source.id == request.form['source'])\
                   .one()
        phrase_ids = map(int, request.form.getlist('phrases'))
        session.query(Phrase).filter(Phrase.id.in_(phrase_ids))\
                             .delete(synchronize_session='fetch')

        s.content = ' '.join(map(lambda p: p.raw, s.phrases))

        session.commit()

        return redirect('/sources/{}'.format(s.id))

def templates():
    # TODO auth
    method = get_method(request)

    if method == 'POST':
        session = get_session(DEFAULT_DB)
        t = Template(name=request.form['template_name'],
                     lines=json.loads(request.form['template_json']))
        session.add(t)
        session.commit()
        return redirect('/templates/{}'.format(t.id))

    if method == 'GET':
        session = get_session(DEFAULT_DB)
        ts = session.query(Template).all()
        context = {
            'username': 'vilmibm',
            'authenticated': True,
            'templates': ts,
        }
        return render_template('templates.html', **context)

def template(template_id):
    # TODO auth
    method = get_method(request)

    if method == 'PUT':
        session = get_session(DEFAULT_DB)
        t = session.query(Template).filter(Template.id == template_id).one()
        t.name = request.form['template_name']
        t.lines = json.loads(request.form['template_json'])
        session.add(t)
        session.commit()
        return redirect('/templates/{}'.format(template_id))

    if method == 'DELETE':
        session = get_session(DEFAULT_DB)
        session.query(Template).filter(Template.id == template_id).delete()
        session.commit()
        return redirect('/templates')

    if method == 'GET':
        session = get_session(DEFAULT_DB)
        t = session.query(Template).filter(Template.id == template_id).one()
        context = {
            'username': 'vilmibm',
            'authenticated': True,
            'template': t,
        }
        return render_template('template.html', **context)

def generate():
    # TODO auth
    method = get_method(request)

    if method == 'GET':
        session = get_session(DEFAULT_DB)
        corpora = session.query(Corpus).all()
        context = {
            'username': 'vilmibm',
            'authenticated': True,
            'corpora': corpora,
        }
        return render_template('generate.html', **context)
