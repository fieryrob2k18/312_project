from pymongo import MongoClient
import json

class MongoDB:
    def __init__(self, url, dbName, collName):
        client = MongoClient(url)
        database = client[dbName]
        self.collection = database[collName]

    def addOne(self, id, body):
        r = self.collection.insert_one(json.loads(body))
        return json.dumps(r)

    def addMany(self, id, body):
        r = self.collection.insert_many(json.loads(body))
        return json.dumps(r)

    def getOne(self, id, body):
        r = self.collection.find_one({"_id": id})
        return json.dumps(r)

    def updateOne(self, id, body):
        r = self.collection.update_one({"_id": id}, json.loads(body))
        return json.dumps(r)

    def removeOne(self, id, body):
        r = self.collection.delete_one({"_id": id})
        return json.dumps(r)