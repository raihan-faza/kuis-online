

DATABASES = {
    'default': {
        'ENGINE': '',
    }
}

from pymongo import MongoClient

MONGO_CLIENT = MongoClient('your_mongodb_connection_string')
MONGO_DB = MONGO_CLIENT['your_database_name']
MONGO_COLLECTION = MONGO_DB['your_collection_name']
