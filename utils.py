# imports
import os.path
import json
from types import NoneType

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
    imagecounter.updateOne(json.loads(imagecounter.getFirst())["_id"]["$oid"], json.dumps({"mostrecent": aidee + 1}))
    return filename