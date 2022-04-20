from pymongo import MongoClient
import json
import bson.json_util

class MongoDB:
    def __init__(self, url, dbName, collName):
        client = MongoClient(url)
        database = client[dbName]
        self.collection = database[collName]

    def addOne(self, body):
        self.collection.insert_one(json.loads(body))

    def addMany(self, body):
        self.collection.insert_many(json.loads(body))

    def getOne(self, id):
        r = self.collection.find_one({"_id": id})
        return bson.json_util.dumps(r)

    def getFirst(self):
        r = self.collection.find_one({})
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
        new = {"$set": json.loads(body)}
        print(id, body, new, flush=True)
        self.collection.update_one({"_id": id}, new)

    def removeOne(self, id):
        self.collection.delete_one({"_id": id})

# storage for database access
def getDatabases():
# syntax is name -> new object
    return {"usernames": MongoDB("mongo", "users", "usernames"),
             "comments": MongoDB("mongo", "comments", "comments"),
             "imgcnt": MongoDB("mongo", "imgcnt", "imgcnt")}