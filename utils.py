# imports
import os.path

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
        return generateResponse("The requested content does not exist".encode(), "text/plain", "404 Not Found", [])

# takes in the multipart login form and returns the desired pieces
def digestLoginForm(headers, body):
    # headers are decoded, body is still encoded
    boundary = headers["Content-Type"].replace("multipart/form-data; boundary=", "", 1)
    # this is a list of bytes
    encodedparts = body.split(boundary.encode())
    # looking for 'Content-Disposition: form-data; name="username"'
    username = ""
    for part in encodedparts:
        if b'name="username"' in part:
            username = part.decode()
    return username