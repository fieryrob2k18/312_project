from encodings import utf_8


def upgrade(req):
    print(req, flush=True)
    key = req["Sec-WebSocket-Key"]
    return 
