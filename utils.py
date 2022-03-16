# imports

# formats a response based on the inputs, encoding type is utf-8 unless otherwise specified
def generateResponse(responsecode: str, contenttype: str, headers: list[str], body: bytes, encoding="utf-8"):
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
    with open(filename, "rb") as content:
        body = content.read()
        return generateResponse(responsecode, contenttype, ["X-Content-Type-Options:nosniff"], body)