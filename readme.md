# prosaicweb

_being a web frontend to [prosaic](https://github.com/nathanielksmith/prosaic)_.

## prereqs

* python >= 3.5.1
* recent debian / ubuntu
* postgresql >= 9.0
* some build helpers (see `setup.sh`)
* (optional) nginx for reverse proxying to gunicorn

## installation / deploy

```bash
    # get code
    git clone https://github.com/nathanielksmith/prosaicweb
    cd prosaicweb/prosaicweb

    # edit cfg.py and set the secret key
    cp example.cfg.py cfg.py

    # srsly read/review what this is going to do :)
    cd ..
    cat setup.sh
    bash setup.sh

    # run it at port :8000 with gunicorn
    bash run.sh

```

## changelog

* 1.0.0 - kick that old shit to the curb
* 0.0.2 - make it work on webkit, support site_name
* 0.0.1 - initial release. user accounts, upload, template editing, corpus mixing.

## author

vilmibm <nathanielksmith@gmail.com>

## license

AGPL v3
