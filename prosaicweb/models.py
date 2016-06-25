#  prosaicweb
#  Copyright (C) 2016  nathaniel smith
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
from functools import lru_cache

from prosaic.models import Base, Source, Corpus, Phrase, corpora_sources
from prosaic.parsing import process_text
from sqlalchemy import create_engine, Column, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.dialects.postgresql import ARRAY, TEXT, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

class Database(dict):
    def __init__(self, user='prosaic', password='prosaic', host='localhost',
                 port=5432, dbname='prosaic'):
        self._data = dict(user=user, password=password, port=port,
                          host=host, dbname=dbname)

    def __getattr__(self, k: str) -> str:
        return self[k]

    def __getitem__(self, k: str) -> str:
        return self._data[k]

    def _fmt(self) -> str:
        return ';'.join(sorted(map(str, self._data.values())))

    def __hash__(self) -> int:
        return hash(self._fmt())

    def __repr__(self) -> str:
        return self._fmt()

DEFAULT_DB = Database(**{'user': 'prosaic',
                  'password': 'prosaic',
                  'host': '127.0.0.1',
                  'port': 5432,
                  'dbname': 'prosaic'})

@lru_cache(maxsize=128)
def get_engine(db: Database) -> Engine:
    return create_engine('postgresql://{user}:{password}@{host}:{port}/{dbname}'\
           .format(**db))

Session = sessionmaker()

def get_session(db: Database):
    Session.configure(bind=get_engine(db))
    return Session()

users_sources = Table('users_sources', Base.metadata,
                    Column('user_id', INTEGER, ForeignKey('users.id')),
                    Column('source_id', INTEGER, ForeignKey('sources.id')))

users_corpora = Table('users_corpora', Base.metadata,
                    Column('user_id', INTEGER, ForeignKey('users.id')),
                    Column('corpus_id', INTEGER, ForeignKey('corpora.id')))

users_templates = Table('users_templates', Base.metadata,
                    Column('user_id', INTEGER, ForeignKey('users.id')),
                    Column('template_id', INTEGER, ForeignKey('templates.id')))

class Template(Base):
    __tablename__ = 'templates'

    id = Column(INTEGER, primary_key=True)
    # TODO

class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True)
    username = Column(TEXT)
    pwhash = Column(TEXT)
    email = Column(TEXT)

    sources = relationship('Source', secondary=users_sources)
    corpora = relationship('Corpus', secondary=users_corpora)
    templates = relationship('Template', secondary=users_templates)

    def __repr__(self) -> str:
        return "User(username='{}', email='{}', pwhash='{}')".format(
            self.username, self.email, self.pwhash)

