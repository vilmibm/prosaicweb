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
from . import views
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
    ('/', 'index', views.index, {}),

    ('/generate', 'generate', views.generate,
     {'methods': ['GET', 'POST']}),

    ('/corpora', 'corpora', views.corpora,
     {'methods': ['GET', 'POST',]}),

    ('/sources', 'sources', views.sources,
     {'methods': ['GET', 'POST',]}),

    ('/sources/<source_id>', 'source', views.source,
     {'methods': ['GET', 'PUT', 'POST', 'DELETE']}),

    ('/corpora/<corpus_id>', 'corpus', views.corpus,
     {'methods': ['GET', 'PUT', 'POST', 'DELETE']}),

    ('/templates', 'templates', views.templates,
     {'methods': ['GET', 'POST', 'DELETE', 'PUT']}),

    ('/auth/account', 'account', account,
     {'methods': ['GET', 'POST', 'DELETE', 'PUT']}),

    ('/auth/session', 'session', session,
     {'methods': ['POST', 'DELETE']}),
]


for [route, name, fn, opts] in routes:
    app.add_url_rule(route, name, fn, **opts)

if __name__ == '__main__': app.run()
