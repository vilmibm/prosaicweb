from uuid import uuid1

class Corpus:
    def __init__(self, name, body):
        self.id = uuid1()
        self.name = name
        self.body = body
