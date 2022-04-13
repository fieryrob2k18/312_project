#temporary storage for users
#keys are usernames, values are lists of comments
#TODO: Replace with proper db calls
users = {}


#Adds comment to users,
#also creates user if necessary
def add_comment(user, comment):
    if users.has_key(user):
        posts = users[user]
        posts += comment
        users[user] = posts
    else:
        users[user] = [comment]


def get_users():
    return users.keys()


def get_comments():
    out = []
    for key in users:
        for comment in users[key]:
            commentstr = key + ": " + comment
            out += commentstr
    return out
