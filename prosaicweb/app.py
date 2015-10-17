from functools import lru_cache

from flask import Flask, render_template, request, redirect
from pyhocon import ConfigFactory
from prosaic.cthulhu import poem_from_template
from pymongo import MongoClient

# TODO https://github.com/zeekay/flask-uwsgi-websocket

from models import Corpus

SITE_NAME = 'prosaicweb'
DEFAULT_CONFIG = './prosaicweb.conf'

app = Flask('prosaicweb')

config = ConfigFactory.parse_file(DEFAULT_CONFIG)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html', **{})

@app.route('/upload', methods=['GET'])
def get_upload():
    context = {
        'corpora': [Corpus('hello', 'foo'),
                    Corpus('there', 'bar'),
                    Corpus('how', 'baz')],
    }
    return render_template('upload.html', **context)

@app.route('/upload', methods=['POST'])
def post_upload():
    pass

@app.route('/generate', methods=['GET'])
def get_generate():
    dbclient = MongoClient()
    # TODO get list of templates
    context = {'templates': ['haiku', 'sonnet', 'sestina'],
               'corpora': dbclient.database_names()}
    return render_template('generate.html', **context)

@app.route('/generate', methods=['POST'])
def post_generate():
    pass

@app.route('/corpora/<corpus_id>', methods=['GET'])
def get_corpora(corpus_id):
    return Corpus('random', 'inventing situations').body

@app.route('/haiku')
def get_haiku():
    db = MongoClient().prettygibson.phrases
    lines = poem_from_template([{'syllables': 5},
                                {'syllables': 7},
                                {'syllables': 5},], db)
    return '<br>'.join(map(lambda l: l['raw'], lines))


if __name__ == '__main__':
    app.run()
