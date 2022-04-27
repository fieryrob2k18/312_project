# imports
import sys
import json
from websocket import upgrade
import utils as u
import template as t
import mongo as m

# debug
DEBUG = True

# storage for database access
# syntax is name -> new object
databases = {"usernames": m.MongoDB("mongo", "users", "usernames"),
             "comments": m.MongoDB("mongo", "comments", "comments"),
             "imgcnt": m.MongoDB("mongo", "imgcnt", "imgcnt")}


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
        # image url
        case "image":
            return u.sendFile("files/image/" + splitpath[1], "image/jpeg")
        # login form submission
        case "login-form":
            if requestmethod == "POST":
                username = u.digestForm(headers, body, ["username"])["username"].decode()
                if DEBUG:
                    print(username, flush=True)
                # put username in database
                databases["usernames"].addOne(json.dumps({"username": username}))
                # redirect user to main page
                return u.generateResponse("".encode(), "", "303 See Other", ["Location: /main"])
        # pfp upload form submission
        case "image-upload":
            if requestmethod == "POST":
                imagebytes = u.digestForm(headers, body, ["upload"])["upload"]
                # save image
                filename = u.saveImage(imagebytes, databases["imgcnt"]) if imagebytes != b"" else ""
                if DEBUG:
                    print(filename, flush=True)
                    return u.sendFile("files/" + filename, "image/jpeg")
                # TODO add filename to users database once username is associated
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
        #stylesheet
        case "goosestyle.css":
            with open("files/goosestyle.css", "rb") as content:
                html = content.read()
            return u.generateResponse(t.renderHtmlTemplate(html), "text/css", "200 OK", [])
        # default user profile image
        case "default.jpg":
            with open("files/default.jpg", "rb") as content:
                outimg = content.read()
            return u.generateResponse(outimg, "image/jpeg", "200 OK", ["X-Content-Type-Options: nosniff"])
        #background image for style
        case "background.jpg":
            with open("files/background.jpg", "rb") as content:
                outimg = content.read()
            return u.generateResponse(outimg, "image/jpeg", "200 OK", ["X-Content-Type-Options: nosniff"])
        # path of /functions.js
        case "functions.js":
            with open("files/functions.js", "rb") as content:
                file = content.read()
            return u.sendFile("files/functions.js", "text/javascript")
        # Websocket handshake
        case "websocket":
            return u.generateResponse("".encode(), "", "101 Switching Protocols", upgrade(headers))
        #Getting chat history
        case "chat-history":
            chatJson = u.getChatHistory(databases["comments"])
            return u.generateResponse(chatJson, "application/json", "200 OK", [])
        # if the path doesn't match anything (404)
        case _:
            return u.sendFile("files/notfound.html", "text/html", "404 Not Found")
