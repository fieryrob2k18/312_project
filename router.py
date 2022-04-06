# imports
import sys
import utils as u
import template as t

# debug
DEBUG = True

# storage for dynamic database access
# syntax is name -> new object
# TODO actually create database objects
databases = {}

# requestmethod is GET, POST, etc
# path is requested path
# body is anything after \r\n\r\n
# headers is the dict of headers
def routeToResponse(requestmethod, path, body, headers):
    # break path down by removing first / and splitting by /
    # i.e. /test/test2/test3 -> test, test2, test3
    # home path ("/") will be a list with a single empty string in it
    splitpath = path.strip("/").split("/")
    # if first part of path is a database name
    if splitpath[0] in databases:
        databasename = splitpath[0]
        # TODO decide what to do if prompt is None, if anything
        prompt = splitpath[1] if len(splitpath) > 1 else None
        match requestmethod:
            # TODO: actually save the returned info and do something with it
            case "GET":
                databasename.get(prompt, body)
            case "POST":
                databasename.post(prompt, body)
    # otherwise
    else:
        match splitpath[0]:
            # login form submission
            # TODO this should probably be moved to database code above
            case "login-form":
                username = u.digestLoginForm(headers, body)
                if DEBUG:
                    print(username)
                    sys.stdout.flush()
                    sys.stderr.flush()
                # TODO put username in database
                return u.generateResponse("".encode(), "", "303 See Other", ["Location: /"])
            # path of /
            case "":
                with open("files/index.html", "rb") as content:
                    html = content.read()
                return u.generateResponse(t.renderHtmlTemplate(html), "text/html", "200 OK", [])
            # if the path doesn't match anything (404)
            case _:
                return u.sendFile("files/notfound.html", "text/html", "404 Not Found")