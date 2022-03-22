from os import environ
from pymongo import MongoClient
import environ


class db_connector():
    env = environ.Env()
    client = MongoClient(
        f'mongodb+srv://{env("DATABASE_USER")}:{env("DATABASE_PASS")}@streamix.zfoco.mongodb.net/{env("DATABASE_NAME")}?retryWrites=true&w=majority')
    db_handle = client['Streamix']
