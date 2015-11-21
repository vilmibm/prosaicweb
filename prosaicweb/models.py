'''i don't even like this real talk'''
from pymongo import MongoClient

DBNAME = 'prosaicweb'

# TODO lru cache
# ideally these would be static class things inside Model:
def client():
    return MongoClient()

def db():
    return client()[DBNAME]

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
        # TODO mongo find_one?
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
    col = db().phrases

    # TODO kill me
    @classmethod
    def find_one(klass, **kwargs):
        source_name = kwargs.get('name', None)
        if not source_name:
            return None

        matching = list(filter(lambda n: source_name == n, klass.list_names()))

        if matching:
            return {'name': matching[0]}

    @classmethod
    def list_names(klass):
        return klass.col.distinct('source')

class User(Model):
    col = db().users

    @property
    def uploads_locked(self):
        return self.col.find_one(**self.data).get('uplpoads_locked', False)

    def lock_uploads(self):
        self.data['uploads_locked'] = True
        self.save()

    def unlock_uploads(self):
        self.data['uploads_locked'] = False
        self.save()


