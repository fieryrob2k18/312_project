from pymongo import MongoClient
import json
import bson.json_util

class MongoDB:
    def __init__(self, url, dbName, collName):
        client = MongoClient(url)
        database = client[dbName]
        self.collection = database[collName]

    def addOne(self, id, body):
        self.collection.insert_one(json.loads(body))

    def addMany(self, id, body):
        self.collection.insert_many(json.loads(body))

    def getOne(self, id, body):
        r = self.collection.find_one({"_id": id})
        return bson.json_util.dumps(r)

    def updateOne(self, id, body):
        self.collection.update_one({"_id": id}, json.loads(body))

    def removeOne(self, id, body):
        self.collection.delete_one({"_id": id})