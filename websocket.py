import base64
from encodings import utf_8
import hashlib
import json
import random

from tomli import TOMLDecodeError

activeConnections = {}

def upgrade(req):
    key = req["Sec-WebSocket-Key"]
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    hash = hashlib.sha1((key + GUID).encode()).digest()
    hash = base64.b64encode(hash)
    return [
        "Connection: Upgrade",
        "Upgrade: websocket",
        "Sec-WebSocket-Accept: " + hash.decode(),
    ]


def webSocketServer(conn):
    while True:
        username = "goose#" + str(random.randint(0, 10000))
        activeConnections[username] = conn
        buffer = conn.recv(1024)
        opcode = buffer[0] & 15
        maskBit = (buffer[1] & 128) / 128
        length = buffer[1] & 127
        mask = []
        payloadIndex = 2
        if length == 126:
            # Length is the next 16 bytes
            length = int.from_bytes(buffer[2:4], "big")
            payloadIndex = 4

        if length == 127:
            # Length is the next 64 bytes
            length = int.from_bytes(buffer[2:10], "big")
            payloadIndex = 10

        if length > 1024:
            # See if we need to get more data
            while length > len(buffer):
                newBuffer = conn.recev(1024)
                buffer.append(newBuffer)

        if maskBit == 1:
            # Get mask if needed
            mask = buffer[payloadIndex : payloadIndex + 4]
            payloadIndex = payloadIndex + 4

        payload = bytearray(buffer[payloadIndex : payloadIndex + length])

        if maskBit == 1:
            # Demask payload if needed
            counter = 0
            for index in range(0, len(payload)):
                payload[index] = payload[index] ^ mask[counter]
                counter = counter + 1
                if counter == 4:
                    counter = 0

        if opcode == 8:
            del activeConnections[username]
            frame = makeFrame("")
            conn.send(frame)
            return

        if opcode == 1:
            # Format is text
            data = json.loads(payload)
            if data["messageType"] == "chatMessage":
                messageText = data["comment"]
                response = json.dumps(
                    {
                        "messageType": "chatMessage",
                        "username": username,
                        "comment": messageText,
                    }
                )
                frame = makeFrame(response)
                for c in activeConnections.items():
                    c[1].send(frame)

        if opcode == 2:
            # Format is binary
            return


def makeFrame(payload):
    length = len(payload)
    payloadIndex = 2

    sizeLength = 0
    if length < 126:
        sizeLength = 2
    elif length >= 126 and length < 65536:
        sizeLength = 4
    elif length >= 65536:
        sizeLength = 10

    frame = bytearray(length + sizeLength)
    if length == 0:
        #Check if we want to terminate the connection
        frame[0] = 136
    else:
        frame[0] = 129

    if length < 126:
        frame[1] = length
    elif length >= 126 and length < 65536:
        frame[1] = 126
        frame[2:4] = length
        payloadIndex = 4
    elif length >= 65536:
        frame[1] = 127
        frame[2:10] = length
        payloadIndex = 10

    for b in payload:
        #I fucking hate python
        frame[payloadIndex] = int.from_bytes(b.encode("utf-8"), "big")
        payloadIndex = payloadIndex + 1

    return frame
