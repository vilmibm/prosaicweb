from functools import lru_cache
from pymongo import MongoClient

import cfg

@lru_cache(maxsize=None)
def client():
    return MongoClient()

def db():
    return client()[cfg.DBNAME]
