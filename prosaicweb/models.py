'''i don't even like this real talk'''
from uuid import uuid1
from pymongo import MongoClient

class Model:
    # class methods
    def list_names():
        """list of the names of all things of this type"""
        pass

    def list():
        """list all of models of this type"""
        pass

    def find(attrs):
        pass

    # instance methods
    def __init__(self, collection, data, docid=None):
        self.data = data
        self.col = collection
        self._id = docid

    def save(self):
        self.col.insert_one()
        pass


class Corpus:
    def __init__(self, name, body):
        self.id = uuid1()
        self.name = name
        self.body = body

    def get(corpus_id):
        # TODO look up by id, instantiate
        return Corpus('todo', 'todo')

class Source:
    pass

class Template:
    pass
