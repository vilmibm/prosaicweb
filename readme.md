# prosaicweb

_being a web frontend to [prosaic](https://github.com/nathanielksmith/prosaic)_.

# design

## mvp

* visiting the site creates a session for you
* can only have one queued upload per session
* can only have one queued poetry generation per session
* saves generated poetry for 7 days (can be deleted sooner)
* editor for templates (basic textarea is fine)

## future

* richer editor for syntax
* ability to pin lines in generated poem, keep generating

# architecture

* some kind of job queue (mongodb+celery? or redis+celery?)
* flask webapp
* gunicorn server
* mongodb; easier just because it has to exist for prosaic

# urls

## mvp

* /: landing page. links for "upload corpus" or "generate poetry"
* /upload: upload text file, paste text. use/create session. label with "file name", description
* /generate: pick corpora, generate poem. use/create session.

## future

* /poetry: all generated poems
* /corpora: all corpora, listed with details
