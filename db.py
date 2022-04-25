
from tinydb import TinyDB, Query

db = TinyDB('db.json')

from_user = input('how much ')
db.insert({'user1': from_user})

user = Query()

vm = db.search(user.user1 == 'y')
