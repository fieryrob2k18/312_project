# imports
import os.path
from types import NoneType
import mongo as m
import html
import bcrypt
import hashlib
import random
import string
import json

DEBUG = True

# does what it says on the tin and saves the token in database
def generateAuthToken(username, database):
    characterbank = string.ascii_letters + string.digits
    token = "".join(random.choices(characterbank, k=30))
    hashed = hashlib.sha256(token.encode()).digest()
    database.addOne({"username": username, "token": hashed})
    return token

# does what it says on the tin
def checkAuthToken(token: str, database):
    hashed = hashlib.sha256(token.encode()).digest()
    result = json.loads(database.getMany("token", hashed))
    if not result:
        return None
    else:
        return result[0]["username"]

# takes digestForm map and usernames database and checks for correct login
def handleLogin(userpassmap, userbase):
    username = html.escape(userpassmap["username"].decode())
    password = userpassmap["password"]
    result = json.loads(userbase.getMany("username", username))
    if not result:
        return None
    print(result[0], flush=True)
    if bcrypt.checkpw(password, result[0]["password"].encode()):
        return username

# takes digestForm map and usernames database and html escapes username and salts/hashes pass before storing both
def handleRegister(userpassmap, userbase):
    username = html.escape(userpassmap["username"].decode())
    # TODO check if username exists and deny "overwrite"
    password = userpassmap["password"]
    hashedpass = bcrypt.hashpw(password, bcrypt.gensalt())
    if DEBUG:
        print(username, flush=True)
    # put username and hashed password in database
    userbase.addOne({"username": username, "password": hashedpass.decode()})

# formats a response based on the inputs, encoding type is utf-8 unless otherwise specified
def generateResponse(body: bytes, contenttype: str, responsecode: str, headers: list[str], encoding="utf-8"):
    contentlength = len(body)
    response = b'HTTP/1.1 ' + responsecode.encode(encoding)
    response += b'\r\nContent-Length: ' + str(contentlength).encode(encoding)
    if contentlength != 0:
        response += b'\r\nContent-Type: ' + contenttype.encode(encoding)
    for header in headers:
        response += b'\r\n' + header.encode(encoding)
    response += b'\r\n\r\n'
    response += body
    return response

# wrapper for generate response that formats a file in the body, 200 OK code is assumed unless otherwise specified
def sendFile(filename, contenttype, responsecode="200 OK"):
    if os.path.isfile(filename):
        with open(filename, "rb") as content:
            body = content.read()
            return generateResponse(body, contenttype, responsecode, ["X-Content-Type-Options:nosniff"])
    # if file is not found
    else:
        with open("files/notfound.html", "rb") as content:
            body = content.read()
            return generateResponse(body, "text/html", "404 Not Found", ["X-Content-Type-Options:nosniff"])

# takes in a multipart form and returns the desired pieces, still encoded
def digestForm(headers, body, desiredparts: list[str]):
    # headers are decoded, body is still encoded
    boundary = headers["Content-Type"].replace("multipart/form-data; boundary=", "", 1)
    # this is a list of bytes
    encodedparts = body.split(boundary.encode())
    toreturn = {}
    for part in encodedparts:
        for desired in desiredparts:
            blurb = 'name="'+desired+'"'
            if blurb.encode() in part:
                toreturn[desired] = part.split(b"\r\n\r\n", 1)[1].strip(b"--").strip()
    return toreturn

# saves an image given the image bytes and the counter database object (for automatic naming)
def saveImage(imagebyes, imagecounter):
    temp = imagecounter.getFirst()
    if temp is None:
        imagecounter.addOne(json.dumps({"mostrecent": 1}))
    aidee = json.loads(imagecounter.getFirst())["mostrecent"]
    # TODO change this to whatever filename prefix is used for sending the images to the client
    filename = "image/pic" + str(aidee) + ".jpg"
    with open("files/" + filename, "wb") as content:
        content.write(imagebyes)
    imagecounter.updateOne(json.loads(imagecounter.getFirst())["_id"]["$oid"], {"mostrecent": aidee + 1})
    return filename


#Read chat history, json response
def getChatHistory(db):
    comments = db.getAll()
    print(comments)
    print(type(comments))
    return bytes(comments, "utf-8")
