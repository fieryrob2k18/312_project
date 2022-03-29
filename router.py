# imports
import utils as u

# storage for dynamic database access
# syntax is name -> new object
# TODO actually create database objects
databases = {}

# requestmethod is GET, POST, etc
# path is requested path
# body is anything after \r\n\r\n
def routeToResponse(requestmethod, path, body):
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
            # path of /
            case "":
                return u.sendFile("files/index.html", "text/html")
            # if the path doesn't match anything (404)
            case _:
                return u.sendFile("files/notfound.html", "text/html", "404 Not Found")