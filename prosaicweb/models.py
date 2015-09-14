from uuid import uuid1

class Corpus:
    def __init__(self, name, body):
        self.id = uuid1()
        self.name = name
        self.body = body

    def get(corpus_id):
        # TODO look up by id, instantiate
        return Corpus('todo', 'todo')
