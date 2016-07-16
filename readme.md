# prosaicweb

_being a web frontend to [prosaic](https://github.com/nathanielksmith/prosaic)_.

## requirements

* python >= 3.5.1
* recent debian / ubuntu
* (optional) nginx for reverse proxying to gunicorn

## installation / deploy

```bash
    # get code
    git clone https://github.com/nathanielksmith/prosaicweb
    cd prosaicweb/prosaicweb

    # edit cfg.py and set the secret key
    cp example.cfg.py cfg.py

    # srsly read/review what this is going to do :)
    cat setup.sh
    bash setup.sh

    # run it at port :8000 with gunicorn
    bash run.sh

```

    # install initial text sources
    python -c 'from fixtures import install; install()'

    # run. should prob reverse proxy.
    gunicorn app:app -D -b 0.0.0.0:8000

## changelog

* 1.0.0 - kick that old shit to the curb
* 0.0.2 - make it work on webkit, support site_name
* 0.0.1 - initial release. user accounts, upload, template editing, corpus mixing.

## author

vilmibm <nathanielksmith@gmail.com>

## license

AGPL v3
