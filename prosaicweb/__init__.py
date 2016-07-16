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
import sys

from . import views
from .cfg import DB
from .models import Base, get_engine,Database
from .views.auth import login, logout,  register
from .app import app, bcrypt

routes = [
    # TODO
    # because html is dumb and forms can only use post/get, that's all we take
    # here. However, within each view function, we check for a _method on a
    # POST and treat that as the method. This should really be handled by a
    # middleware.
    ('/', 'index', views.index, {}),
    ('/generate', 'generate', views.generate, {'methods': ['GET', 'POST']}),
    ('/corpora', 'corpora', views.corpora, {'methods': ['GET', 'POST',]}),
    ('/sources', 'sources', views.sources, {'methods': ['GET', 'POST',]}),
    ('/sources/<source_id>', 'source', views.source,
     {'methods': ['GET', 'POST']}),
    ('/corpora/<corpus_id>', 'corpus', views.corpus,
     {'methods': ['GET', 'POST']}),
    ('/phrases', 'phrases', views.phrases, {'methods': ['POST']}),
    ('/templates', 'templates', views.templates, {'methods': ['GET', 'POST']}),
    ('/templates/<template_id>', 'template', views.template,
     {'methods': ['GET', 'POST']}),
    ('/auth/login', 'login', login, {'methods': ['POST']}),
    ('/auth/register', 'register', register, {'methods':['GET', 'POST']}),
    ('/auth/logout', 'logout', logout, {}),
]

for [route, name, fn, opts] in routes:
    app.add_url_rule(route, name, fn, **opts)

def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == 'dbinit':
        print('initializing prosaic and prosaicweb database state...')
        Base.metadata.create_all(bind=get_engine(Database(**DB)))
        exit(0)

    app.run()

if __name__ == '__main__':
    main()
