from pymongo import MongoClient
import bson.json_util
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self, url, dbName, collName):
        client = MongoClient(url)
        database = client[dbName]
        self.collection = database[collName]

    def addOne(self, body):
        r = self.collection.insert_one(body)
        return r.inserted_id

    def addMany(self, body):
        self.collection.insert_many(body)

    def getOne(self, id):
        r = self.collection.find_one({"_id": id})
        return bson.json_util.dumps(r)

    def getFirst(self):
        r = self.collection.find_one({})
        if r is None:
            return None
        else:
            return bson.json_util.dumps(r)

    def getMany(self, key, value):
        r = list(self.collection.find({key: value}))
        return bson.json_util.dumps(r)

    def getAll(self):
        allrecs = self.collection.find({})
        result = []
        for entry in allrecs:
            result.append(entry)
        return bson.json_util.dumps(result)

    def updateOne(self, id, body):
        new = {"$set": body}
        self.collection.update_one({"_id": ObjectId(id)}, new)

    def removeOne(self, id):
        self.collection.delete_one({"_id": id})