from functools import lru_cache
from flask import Flask, render_template, request, redirect
from pyhocon import ConfigFactory
# TODO https://github.com/zeekay/flask-uwsgi-websocket

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
    return "index"

@app.route('/upload', methods=['GET'])
def get_upload():
    return "upload a thing"

@app.route('/upload', methods=['POST'])
def post_upload():
    pass

@app.route('/generate', methods=['GET'])
def get_generate():
    return "generate a thing"

@app.route('/generate', methods=['POST'])
def post_generate():
    pass

if __name__ == '__main__':
    # TODO take option:
    app.config['CONFIG_PATH'] = DEFAULT_CONFIG
    app.run()
