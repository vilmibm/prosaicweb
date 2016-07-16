# flask debug
DEBUG = False

# set to something real
SECRET_KEY = 'skreeeeekettttttttt yo'

# probably fine
MAX_UPLOAD_SIZE = 5 * 1024 * 1024 # 5mb

# this is what you want most likely; it's prosaic's default and you share a db
DB = {
    'user': 'prosaic',
    'password': 'prosaic',
    'host': '127.0.0.1',
    'port': 5432,
    'dbname': 'prosaic'
}
