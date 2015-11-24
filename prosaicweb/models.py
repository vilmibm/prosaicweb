'''i don't even like this real talk'''
from prosaic.nyarlathotep import process_text

from storage import db

class Model:
    col = None # Override in subclasses

    @classmethod
    def list_names(klass):
        """list of the names of all things of this type"""
        things = klass.list()
        return list(map(lambda t: t['name'], things))

    @classmethod
    def list(klass):
        """list all of models of this type"""
        return list(klass.col.find({}))

    @classmethod
    def find(klass, **kwargs):
        return list(klass.col.find(kwargs))

    @classmethod
    def find_one(klass, **kwargs):
        found = klass.find(**kwargs)
        if len(found) > 0:
            return found[0]
        return None

    def __init__(self, data):
        self.data = data

    def save(self):
        self.col.update({'name':self.data['name']}, self.data, True)

class Template(Model):
    col = db().templates

class Source(Model):
    col = db().sources

    def process(self):
        phrases_col = db().phrases
        process_text(self.data['text'], self.data['name'], phrases_col)

class User(Model):
    col = db().users

    @property
    def uploads_locked(self):
        return self.col.find_one(**self.data).get('uploads_locked', False)

    def lock_uploads(self):
        self.data['uploads_locked'] = True
        self.save()

    def unlock_uploads(self):
        self.data['uploads_locked'] = False
        self.save()
