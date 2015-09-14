from functools import lru_cache
from flask import Flask, render_template, request, redirect
from pyhocon import ConfigFactory
# TODO https://github.com/zeekay/flask-uwsgi-websocket

from models import Corpus

SITE_NAME = 'prosaicweb'
# TODO should be something in /etc or whatever
DEFAULT_CONFIG = './prosaicweb.conf'

app = Flask('prosaicweb')

@lru_cache()
def conf_file(path):
    return ConfigFactory.parse_file(path)

def cfg(k):
    config = conf_file(app.config['CONFIG_PATH'])
    return config[k]

@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html', **{})

@app.route('/upload', methods=['GET'])
def get_upload():
    context = {
        "corpora": [Corpus("hello", "foo"),
                    Corpus("there", "bar"),
                    Corpus("how", "baz")],
    }
    return render_template('upload.html', **context)

@app.route('/upload', methods=['POST'])
def post_upload():
    pass

@app.route('/generate', methods=['GET'])
def get_generate():
    return "generate a thing"

@app.route('/generate', methods=['POST'])
def post_generate():
    pass

@app.route('/corpora/<corpus_id>', methods=['GET'])
def get_corpora(corpus_id):
    return Corpus('random', 'inventing situations').body

if __name__ == '__main__':
    # TODO take option:
    app.config['CONFIG_PATH'] = DEFAULT_CONFIG
    app.config['DEBUG'] = True
    app.run()
