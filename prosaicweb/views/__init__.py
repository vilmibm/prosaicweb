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
from flask_login import login_required, current_user
from prosaic.parsing import process_text
from prosaic.generation import poem_from_template

# TODO don't use DEFAULT_DB
from ..models import Source, Corpus, get_session, DEFAULT_DB, corpora_sources, Phrase, Template
from ..util import get_method, auth_context

UNAUTHORIZED = Response(status=401)

# TODO types?
def index():
    return render_template('index.html', **auth_context(request))

@login_required
def corpora():
    method = get_method(request)
    session = get_session(DEFAULT_DB)

    if method == 'GET':
        context = auth_context(request)
        context.update({'corpora': session.query(Corpus).all(),
                        'sources': session.query(Source).all(),})
        return render_template('corpora.html', **context)

    if method == 'POST':
        c = Corpus()
        c.name = request.form['corpus_name']
        c.description = request.form['corpus_description']
        for source_id in request.form.getlist('sources'):
            s = session.query(Source).filter(Source.id==source_id).one()
            c.sources.append(s)
        session.add(c)
        session.commit()
        return redirect('corpora/{}'.format(c.id))

@login_required
def corpus(corpus_id):
    method = get_method(request)
    session = get_session(DEFAULT_DB)

    if method == 'GET':
        context = auth_context(request)
        c = session.query(Corpus).filter(Corpus.id == corpus_id).one()
        source_ids = map(lambda s: s.id, c.sources)

        other_sources = session.query(Source)\
                               .filter(Source.id.notin_(source_ids))\
                               .all()
        context.update({
            'corpus': c,
            'other_sources': other_sources,
        })
        return render_template('corpus.html', **context)

    if method == 'PUT':
        c = session.query(Corpus).filter(Corpus.id == corpus_id).one()
        c.name = request.form['corpus_name']
        c.description = request.form['corpus_description']
        source_ids = map(int, request.form.getlist('sources'))
        c.sources = session.query(Source).filter(Source.id.in_(source_ids)).all()
        session.commit()

        return redirect('/corpora')

    if method == 'DELETE':
        c = session.query(Corpus).filter(Corpus.id == corpus_id).one()
        c.sources = []
        session.commit()
        session.query(Corpus).filter(Corpus.id == corpus_id).delete()
        session.commit()

        return redirect('/corpora')

@login_required
def sources():
    method = get_method(request)
    session = get_session(DEFAULT_DB)

    if method == 'GET':
        context = auth_context(request)
        sources = session.query(Source).all()
        for source in sources:
            source.content_preview = source.content[0:250] + '...'
        context.update({'sources':sources})

        return render_template('sources.html', **context)

    if method == 'POST':
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

@login_required
def source(source_id):
    method = request.form.get('_method', request.method)
    session = get_session(DEFAULT_DB)

    if method == 'GET':
        context = auth_context(request)
        s = session.query(Source).filter(Source.id == source_id).one()
        context.update({
            'source':s,
        })
        return render_template('source.html', **context)

    if method == 'PUT':
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

@login_required
def phrases():
    method = get_method(request)
    session = get_session(DEFAULT_DB)

    if method == 'DELETE':
        s = session.query(Source)\
                   .filter(Source.id == request.form['source'])\
                   .one()
        phrase_ids = map(int, request.form.getlist('phrases'))
        session.query(Phrase).filter(Phrase.id.in_(phrase_ids))\
                             .delete(synchronize_session='fetch')

        s.content = ' '.join(map(lambda p: p.raw, s.phrases))

        session.commit()

        return redirect('/sources/{}'.format(s.id))

@login_required
def templates():
    method = get_method(request)
    session = get_session(DEFAULT_DB)

    if method == 'GET':
        context = auth_context(request)
        ts = session.query(Template).all()
        context.update({
            'templates': ts,
        })
        return render_template('templates.html', **context)

    if method == 'POST':
        t = Template(name=request.form['template_name'],
                     lines=json.loads(request.form['template_json']))
        session.add(t)
        session.commit()
        return redirect('/templates/{}'.format(t.id))

@login_required
def template(template_id):
    method = get_method(request)
    session = get_session(DEFAULT_DB)

    if method == 'GET':
        context = auth_context(request)
        t = session.query(Template).filter(Template.id == template_id).one()
        context.update({
            'template': t,
        })

        return render_template('template.html', **context)

    if method == 'PUT':
        t = session.query(Template).filter(Template.id == template_id).one()
        t.name = request.form['template_name']
        t.lines = json.loads(request.form['template_json'])
        session.add(t)
        session.commit()
        return redirect('/templates/{}'.format(template_id))

    if method == 'DELETE':
        session.query(Template).filter(Template.id == template_id).delete()
        session.commit()
        return redirect('/templates')

@login_required
def generate():
    method = get_method(request)
    session = get_session(DEFAULT_DB)

    if method == 'GET':
        context = auth_context(request)
        cs = session.query(Corpus).all()
        ts = session.query(Template).all()
        context.update({
            'corpora': cs,
            'templates': ts,
        })
        return render_template('generate.html', **context)

    if method == 'POST':
        corpus_id = request.form['corpus_id']
        corpus_name = session.query(Corpus.name)\
                             .filter(Corpus.id==corpus_id)\
                             .one()[0]
        t = json.loads(request.form['template_tweak'])
        poem = poem_from_template(t, DEFAULT_DB, corpus_id)
        source_ids = set(map(lambda p: p[1], poem))
        get_source_name = lambda sid:\
                          session.query(Source.name).filter(Source.id==sid).one()[0]
        ss = map(
            lambda sid: {'id':sid, 'name': get_source_name(sid)},
            source_ids
        )

        result = {
            'corpus': {
                'id': corpus_id,
                'name': corpus_name,
            },
            'lines': list(map(lambda p: p[0], poem)),
            'used_sources': list(ss),
        }

        return json.dumps(result)
