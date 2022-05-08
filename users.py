import mongo as m
import sys
import json

#TODO: Update to work with Rin's db code
databases = {"usernames": m.MongoDB("mongo", "users", "usernames"),
             "comments": m.MongoDB("mongo", "comments", "comments")}

def get_users():
    users = json.loads(databases["usernames"].getAll())
    #print(users)
    #print(type(users))
    #sys.stdout.flush()
    #sys.stderr.flush()
    if len(users) == 0:
        return []
    out = {}
    for user in users:
        if user.has_key("profilepic"):
            out[user["username"]] = user["profilepic"]
        else:
            out[user["username"]]= ""
    return out


#TODO: Fix this
def get_comments():
    return ""
    out = []
    for key in users:
        for comment in users[key]:
            commentstr = key + ": " + comment
            out += commentstr
    return out
