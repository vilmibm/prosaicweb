# prosaicweb

_being a web frontend to [prosaic](https://github.com/nathanielksmith/prosaic)_.

## requirements

* python >= 3.4
* mongodb installed and running
* gcc (for python deps)
* (optional) nginx for reverse proxying to gunicorn

## installation / deploy

    # clone repo
    git clone https://github.com/nathanielksmith/prosaicweb
    cd prosaicweb/prosaicweb

    # set up virtualenv
    virtualenv prosaicwebvenv -p $(which python3)
    source prosaicwebvenv/bin/activate
    pip install -r ../requirements.txt

    # configure
    cp example.cfg.py cfg.py
    # edit cfg.py and set the secret key

    # install initial text sources
    python -c 'from fixtures import install; install()'

    # run. should prob reverse proxy.
    gunicorn app:app -D -b 0.0.0.0:8000

## changelog

* 0.0.2 - make it work on webkit, support site_name
* 0.0.1 - initial release. user accounts, upload, template editing, corpus mixing.

## author

vilmibm <nathanielksmith@gmail.com>

## license

AGPL v3
