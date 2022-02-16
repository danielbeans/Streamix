from pymongo import MongoClient


class db_connector():
    client = MongoClient(
        'mongodb+srv://daniel:CWWXkPRk0iEY9qUw@streamix.zfoco.mongodb.net/Streamix?retryWrites=true&w=majority')
    db_handle = client['Streamix']
