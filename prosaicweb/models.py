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
    def find(klass, attrs):
        return list(klass.col.find(attrs))

    def __init__(self, data):
        self.data = data

    def save(self):
        self.col.update({'name':self.data['name']}, self.data, True)

class Template(Model):
    col = db().templates

class Corpus(Model):
    @classmethod
    def list_names(klass):

        # TODO filter
        return client().database_names()

class Source(Model):
    pass
