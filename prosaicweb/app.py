import json
from functools import lru_cache

from flask import Flask, render_template, request, redirect, jsonify
from pyhocon import ConfigFactory
from prosaic.cthulhu import poem_from_template
from pymongo import MongoClient

# TODO https://github.com/zeekay/flask-uwsgi-websocket

from models import Template, Source

SITE_NAME = 'prosaicweb'
DEFAULT_CONFIG = './prosaicweb.conf'

app = Flask('prosaicweb')

config = ConfigFactory.parse_file(DEFAULT_CONFIG)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html', **{})

@app.route('/generate', methods=['GET'])
def get_generate():
    templates = [{'name': t['name'],
                  'json': json.dumps(t['lines'])}
                 for t in Template.list()]
    context = {'templates': templates,
               'sources': Source.list_names()}
    return render_template('generate.html', **context)

@app.route('/generate', methods=['POST'])
def post_generate():
    sources = request.form.getlist('source')
    combined_col_name = ''.join(sources)

    db = MongoClient().prosaicweb
    col = db[combined_col_name]

    if col.count() == 0:
        for source in sources:
            source_phrases = db.phrases.find({'source': source})
            for phrase in source_phrases:
                phrase.pop('_id')
                col.insert(phrase)

    template = json.loads(request.form['template_raw'])
    lines = poem_from_template(template, col)
    used_sources = set(map(lambda l: l['source'], lines))
    raw_lines = map(lambda l: l['raw'], lines)

    return jsonify(lines=list(raw_lines), used_sources=list(used_sources))

if __name__ == '__main__':
    app.run()
