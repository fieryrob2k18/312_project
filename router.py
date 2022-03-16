# imports
import utils as u

# storage for dynamic database access
# syntax is name -> new object
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
        match requestmethod:
            case "GET":
                # TODO: actually save the returned info and do something with it
                databases[splitpath[0]].get(splitpath[1], body)
            case "POST":
                databases[splitpath[0]].post(splitpath[1], body)
    # otherwise
    else:
        match splitpath[0]:
            # path of /
            case "":
                return u.sendFile("files/index.html", "text/html")
            # if the path doesn't match anything (404)
            case _:
                return u.sendFile("files/notfound.html", "text/html", "404 Not Found")