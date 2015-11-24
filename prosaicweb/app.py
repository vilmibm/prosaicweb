import json
import random
from functools import lru_cache

from flask import Flask, render_template, request, redirect, jsonify, Response
from pyhocon import ConfigFactory
from prosaic.cthulhu import poem_from_template
from prosaic.nyarlathotep import process_text
from pymongo import MongoClient

# TODO https://github.com/zeekay/flask-uwsgi-websocket

from models import Template, Source, User

SITE_NAME = 'prosaicweb'
DEFAULT_CONFIG = './prosaicweb.conf'
SYSTEM_USER = 'system'

app = Flask('prosaicweb')

config = ConfigFactory.parse_file(DEFAULT_CONFIG)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'TESTING LOL'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # 5mb

def collection_name(sources, truncate):
    """TODO"""
    name = ''.join(sources)
    if truncate is not None:
        name += 'truncated'

    return name

def col_copy(src, dest):
    """given two col cursors, copy everything from src into dest."""
    for item in src:
        item.pop('_id')
        dest.insert(item)

@app.route('/', methods=['GET'])
def get_generate():
    user_name = request.cookies.get('user_name')
    sources = Source.find(uploader=user_name)
    if SYSTEM_USER != user_name:
        sources.extend(Source.find(uploader=SYSTEM_USER))
    sources = list(map(lambda s: {'system': s['uploader'] == SYSTEM_USER,
                                  'name': s['name']},
                       sources))
    sources.sort(key=lambda s:s['name'])
    templates = [{'name': t['name'],
                  'json': json.dumps(t['lines'])}
                 for t in Template.list()]
    context = {'templates': templates,
               'sources': sources,
               'user_name': user_name}
    return render_template('generate.html', **context)

@app.route('/generate', methods=['POST'])
def post_generate():
    truncate = request.form.get('truncate', None)
    sources = request.form.getlist('source')
    combined_col_name = collection_name(sources, truncate)

    db = MongoClient().prosaicweb
    col = db[combined_col_name]

    if col.count() == 0:
        print("creating new collection", sources)
        if truncate is None:
            print("not truncating")
            for source in sources:
                source_phrases = db.phrases.find({'source': source})
                col_copy(source_phrases, col)
        else:
            print("truncating")
            counts = list(map(lambda s: db.phrases.find({'source':s}).count(), sources))
            max_phrases = min(counts)
            # want to skip a random chunk such that i still get max_phrases from the random collections
            for source,count in list(zip(sources, counts)):
                print(source,count)
                if count == max_phrases:
                    print("copying all of", source)
                    source_phrases = db.phrases.find({'source': source})
                    col_copy(source_phrases, col)
                else:
                    print("copying part of ", source)
                    diff = count - max_phrases
                    skip = random.randint(0, diff)
                    source_phrases = db.phrases.find({'source': source}).skip(skip)
                    col_copy(source_phrases, col)

    print("done processing cols")

    template = json.loads(request.form['template_raw'])
    lines = poem_from_template(template, col)
    without_blank = filter(lambda l: False == l['blank'], lines)
    used_sources = set(map(lambda l: l['source'], without_blank))
    raw_lines = map(lambda l: l['raw'], lines)

    return jsonify(lines=list(raw_lines), used_sources=list(used_sources))

@app.route('/upload', methods=['POST'])
def post_upload():
    user_name = request.cookies.get('user_name')
    user = User(User.find_one(name=user_name))
    file_name = request.form['upload_name']

    # TODO json errors
    if not (user_name and user):
        return Response('file upload requires auth', 401)

    # TODO lock timeouts in case of server timeout
    if user.uploads_locked:
        return Response('Already uploading a thing.', 400)

    source = Source.find_one(name=file_name)

    if source is not None:
        # TODO json errors
        return Response('Already a source with that name oops.', 400)

    print('proceeding with upload {} for {}'.format(file_name, user_name))

    try:
        user.lock_uploads()
        content = str(request.files.get('upload').read())
        source = Source({'name':file_name, 'text':content, 'uploader':user_name})
        source.process()
        source.save()
    except Exception as e:
        # TODO content type
        return Response(json.dumps({'exception':e.__str__(), 'error': 'parse_exception'}), 400)
    finally:
        user.unlock_uploads()

    return Response(json.dumps({'name':file_name}))

@app.route('/auth', methods=['GET'])
def get_auth():
    return render_template('auth.html')

@app.route('/register', methods=['POST'])
def post_register():

    user_name = request.form.get('name')
    password = request.form.get('password')
    captcha = request.form.get('captcha')
    context = {}

    print('registering new user', user_name)
    if captcha != 'qux':
        print('captcha failed, erroring')
        context['login_msg'] = 'oops, are you human?'
    else:
        user = User.find_one(name=user_name)
        if user is None:
            print('user not found, creating')
            user = User({'name': user_name,
                         'password': password})
            user.save()
            context['login_msg'] = 'registration complete, yu can log in now'
        else:
            print('user found, erroring')
            context['register_msg'] = 'name is taken, sorry'

    # TODO should do a redirect but lol
    return render_template('auth.html', **context)

@app.route('/login', methods=['POST'])
def post_login():
    user_name = request.form.get('name')
    print('logging in', user_name)
    # TODO hash
    # http://flask.pocoo.org/snippets/54/
    password = request.form.get('password')

    user = User.find_one(name=user_name, password=password)

    if user:
        print('found user, logging in')
        response = redirect('/')
        response.set_cookie('user_name', user_name)
        return response
    else:
        print('did not find user, erroring')
        return render_template('auth.html', login_msg="dunno yu sorry")

@app.route('/logout', methods=['POST', 'GET'])
def post_logout():
    print('logging out user', request.cookies.get('user_name'))
    response = redirect('/')
    response.set_cookie('user_name', '', expires=0)
    return response

if __name__ == '__main__':
    app.run()
