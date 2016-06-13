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
import random

from flask import Flask, render_template, request, redirect, jsonify, Response
from prosaic.generation import poem_from_template

from .cfg import SITE_NAME, DEBUG, SECRET_KEY, MAX_UPLOAD_SIZE
from .models import Template, Source, User
from .storage import get_db
from .views import index, corpora, sources, templates, generate
from .views.auth import session, account


# TODO import route functions
# TODO register each with add_url_rule

"""
for views, considering:
    views/__init__.py # default place for views
    views/auth.py     # login/logout/account stuff

alternatives:
    * stick everything into views.py (maybe)
    * put everything here in app.py (no)

I want this file to be a high level look into the app's topography.

for templates:
    templates/base.html # has auth stuff linked
    templates/corpora.html
    templates/sources.html
    templates/templates.html
    templates/generate.html
    templates/account.html # edit account info

notes:
    * can add new templates from generate page
    * can add new sources to a (new) corpora from generate page

# the generate flow

The ingredients of poetry generation:

    * choosing a corpora
    * choosing a template
    * refining the output

The first two will be confined to the left pane, the final to a right pane.

The base html of the site will have this row at the top:

    | generate | sources | corpora | templates | generate | ... | account

where ... expands to fill available space. each link loads the governing template, which will 
inevitably contain forms that POST etc to edit/add/delete things.


routes:

    (PUT: update, POST: new)

    * GET / - static information page

    * GET /generate
    * POST /generate

    * GET /corpora
    * POST /corpora
    * PUT /corpora
    * DELETE /corpora

    * GET /sources
    * POST /sources
    * DELETE /sources
    * PUT /sources

    * GET /templates
    * POST /templates
    * DELETE /templates
    * PUT /templates

    * GET /auth/account    - account info page
    * GET /auth/account/create - create account page
    * POST /auth/account   - create new accoutn
    * PUT /auth/account    - update account
    * DELETE /auth/account - delete account
    * POST /auth/session   - login
    * DELETE /auth/session - logout

"""

SYSTEM_USER = 'sigh' # TODO no
app = Flask('prosaicweb')

app.config['DEBUG'] = DEBUG
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE

routes = [
    ('/', 'index', index, {}),
    ('/generate', 'generate', generate, {'methods': ['GET', 'POST']}),
    ('/corpora', 'corpora', corpora, {'methods': ['GET', 'POST', 'DELETE', 'PUT']}),
    ('/sources', 'sources', sources, {'methods': ['GET', 'POST', 'DELETE', 'PUT']}),
    ('/templates', 'templates', templates, {'methods': ['GET', 'POST', 'DELETE', 'PUT']}),
    ('/auth/account', 'account', account,
     {'methods': ['GET', 'POST', 'DELETE', 'PUT']}),
    ('/auth/session', 'session', session, {'methods': ['POST', 'DELETE']}),
]

for [route, name, fn, opts] in routes:
    app.add_url_rule(route, name, fn, **opts)

#def collection_name(sources, truncate):
#    """TODO"""
#    name = ''.join(sources)
#    if truncate is not None:
#        name += 'truncated'
#
#    return name
#
#def col_copy(src, dest):
#    """given two col cursors, copy everything from src into dest."""
#    for item in src:
#        item.pop('_id')
#        dest.insert(item)
#
#def get_generate():
#    user_name = request.cookies.get('user_name')
#    sources = Source.find(uploader=user_name)
#    if SYSTEM_USER != user_name:
#        sources.extend(Source.find(uploader=SYSTEM_USER))
#    sources = list(map(lambda s: {'system': s['uploader'] == SYSTEM_USER,
#                                  'name': s['name']},
#                       sources))
#    sources.sort(key=lambda s:s['name'])
#    templates = [{'name': t['name'],
#                  'json': json.dumps(t['lines'])}
#                 for t in Template.list()]
#    context = {'templates': templates,
#               'site_name': SITE_NAME,
#               'sources': sources,
#               'user_name': user_name}
#    return render_template('generate.html', **context)
#
#def post_generate():
#    truncate = request.form.get('truncate', None)
#    sources = request.form.getlist('source')
#    combined_col_name = collection_name(sources, truncate)
#
#    db = get_db()
#    col = db[combined_col_name]
#
#    if col.count() == 0:
#        print("creating new collection", sources)
#        if truncate is None:
#            print("not truncating")
#            for source in sources:
#                source_phrases = db.phrases.find({'source': source})
#                col_copy(source_phrases, col)
#        else:
#            print("truncating")
#            counts = list(map(lambda s: db.phrases.find({'source':s}).count(), sources))
#            max_phrases = min(counts)
#            # want to skip a random chunk such that i still get max_phrases from the random collections
#            for source,count in list(zip(sources, counts)):
#                print(source,count)
#                if count == max_phrases:
#                    print("copying all of", source)
#                    source_phrases = db.phrases.find({'source': source})
#                    col_copy(source_phrases, col)
#                else:
#                    print("copying part of ", source)
#                    diff = count - max_phrases
#                    skip = random.randint(0, diff)
#                    source_phrases = db.phrases.find({'source': source}).skip(skip)
#                    col_copy(source_phrases, col)
#
#    print("done processing cols")
#
#    template = json.loads(request.form['template_raw'])
#    lines = poem_from_template(template, col)
#    without_blank = filter(lambda l: False == l['blank'], lines)
#    used_sources = set(map(lambda l: l['source'], without_blank))
#    raw_lines = map(lambda l: l['raw'], lines)
#
#    return jsonify(lines=list(raw_lines), used_sources=list(used_sources))
#
#def post_upload():
#    user_name = request.cookies.get('user_name')
#    user = User(User.find_one(name=user_name))
#    file_name = request.form['upload_name']
#
#    # TODO json errors
#    if not (user_name and user):
#        return Response('file upload requires auth', 401)
#
#    # TODO lock timeouts in case of server timeout
#    if user.uploads_locked:
#        return Response('Already uploading a thing.', 400)
#
#    source = Source.find_one(name=file_name)
#
#    if source is not None:
#        # TODO json errors
#        return Response('Already a source with that name oops.', 400)
#
#    print('proceeding with upload {} for {}'.format(file_name, user_name))
#
#    try:
#        user.lock_uploads()
#        content = str(request.files.get('upload').read())
#        source = Source({'name':file_name, 'text':content, 'uploader':user_name})
#        source.process()
#        source.save()
#    except Exception as e:
#        # TODO content type
#        return Response(json.dumps({'exception':e.__str__(), 'error': 'parse_exception'}), 400)
#    finally:
#        user.unlock_uploads()
#
#    return Response(json.dumps({'name':file_name}))
#
#def get_auth():
#    return render_template('auth.html', site_name=SITE_NAME)
#
#def post_register():
#
#    user_name = request.form.get('name')
#    password = request.form.get('password')
#    captcha = request.form.get('captcha')
#    context = {}
#
#    print('registering new user', user_name)
#    if captcha != 'qux':
#        print('captcha failed, erroring')
#        context['login_msg'] = 'oops, are you human?'
#    else:
#        user_data = User.find_one(name=user_name)
#        if user_data is None:
#            print('user not found, creating')
#            user = User({'name': user_name,
#                         'password': password})
#            user.save()
#            context['login_msg'] = 'registration complete, yu can log in now'
#        else:
#            print('user found, erroring')
#            context['register_msg'] = 'name is taken, sorry'
#
#    # TODO should do a redirect but lol
#    return render_template('auth.html', **context)
#
#def post_login():
#    user_name = request.form.get('name')
#    print('logging in', user_name)
#    password = request.form.get('password')
#
#    if not (user_name and password):
#        return render_template('auth.html', login_msg="dunno yu sorry")
#
#    user_data = User.find_one(name=user_name)
#    if not user_data:
#        return render_template('auth.html', login_msg="dunno yu sorry")
#    user = User(user_data)
#
#    if user.check_password(password):
#        print('found user, logging in')
#        response = redirect('/')
#        response.set_cookie('user_name', user_name)
#        return response
#    else:
#        print('did not find user, erroring')
#        return render_template('auth.html', login_msg="dunno yu sorry")
#
#def post_logout():
#    print('logging out user', request.cookies.get('user_name'))
#    response = redirect('/')
#    response.set_cookie('user_name', '', expires=0)
#    return response

if __name__ == '__main__': app.run()
