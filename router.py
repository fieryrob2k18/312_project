# imports
import sys
import json
import utils as u
import template as t
import mongo as m

# debug
DEBUG = True

# storage for database access
# syntax is name -> new object
databases = {"usernames": m.MongoDB("mongo", "users", "usernames"),
             "comments": m.MongoDB("mongo", "comments", "comments")}

# requestmethod is GET, POST, etc
# path is requested path
# body is anything after \r\n\r\n
# headers is the dict of headers
def routeToResponse(requestmethod, path, body, headers):
    # break path down by removing first / and splitting by /
    # i.e. /test/test2/test3 -> test, test2, test3
    # home path ("/") will be a list with a single empty string in it
    splitpath = path.strip("/").split("/")
    match splitpath[0]:
        # login form submission
        case "login-form":
            username = u.digestForm(headers, body, ["username"])["username"].decode()
            if DEBUG:
                print(username)
                sys.stdout.flush()
                sys.stderr.flush()
            # put username in database
            databases["usernames"].addOne(0, json.dumps({"username": username}))
            # redirect user to main page
            return u.generateResponse("".encode(), "", "303 See Other", ["Location: /main"])
        # comment form submission
        case "comment-form":
            comment = u.digestForm(headers, body, ["comment"])["comment"].decode()
            if DEBUG:
                print(comment)
                sys.stdout.flush()
                sys.stderr.flush()
            # put comment in database
            databases["comments"].addOne(0, json.dumps({"comment": comment}))
            # redirect user to main page
            return u.generateResponse("".encode(), "", "303 See Other", ["Location: /main"])
        # path of /
        case "":
            with open("files/login.html", "rb") as content:
                html = content.read()
            return u.generateResponse(t.renderHtmlTemplate(html), "text/html", "200 OK", [])
        # path of /main
        case "main":
            with open("files/main.html", "rb") as content:
                html = content.read()
            return u.generateResponse(t.renderHtmlTemplate(html), "text/html", "200 OK", [])
        # if the path doesn't match anything (404)
        case _:
            return u.sendFile("files/notfound.html", "text/html", "404 Not Found")