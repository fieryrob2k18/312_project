// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

let webRTCConnection;

// Allow users to send messages by pressing enter instead of clicking the Send button
document.addEventListener("keypress", function (event) {
    if (event.code === "Enter") {
        sendMessage();
    }
});

// Read the comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
function sendMessage() {
    const chatBox = document.getElementById("chat-comment");
    const comment = chatBox.value;
    chatBox.value = "";
    chatBox.focus();
    if (comment !== "") {
        socket.send(JSON.stringify({ 'messageType': 'chatMessage', 'comment': comment }));
    }
}

function sendDirectMessage() {
    const chatBox = document.getElementById("dm-comment");
    const comment = chatBox.value;
    const userBox = document.getElementById("dm-user");
    const recipient = userBox.value;
    chatBox.value = "";
    chatBox.focus();
    userBox.value = "";
    if (comment !== "") {
        socket.send(JSON.stringify({ 'messageType': 'directMessage', 'comment': comment, 'recipient': recipient }));
    }
}

function upGooseMessage(id) {
    console.log(id)
    if (id !== "") {
        socket.send(JSON.stringify({ 'messageType': 'upGoose', 'id': id }));
    }
}

// Renders a new chat message to the page
function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    chat.innerHTML += "<div id='" + chatMessage["_id"]["$oid"] + "'> <b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<button onclick='upGooseMessage(\""+ chatMessage["_id"]["$oid"] +"\")'> UpGoose! </button></div><br/>";
}

function userList(message) {
    let users = document.getElementById('users');
    users.innerHTML = ""
    for (var user in message["users"]) {
        users.innerHTML += "<b>" + message["users"][user] + "</b>" + "<br/>";
    }
}

function upGoose(message) {
    let upGooseMessage = document.getElementById(message['_id']['$oid'])
    upGooseMessage.innerHTML += "Upgoose"
}a


// called when the page loads to get the chat_history
function get_chat_history() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);
            for (const message of messages) {
                addMessage(message);
            }
        }
    };
    request.open("GET", "/chat-history");
    request.send();
}

// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType

    switch (messageType) {
        case 'chatMessage':
            addMessage(message);
            break;
        case 'upGoose':
            upGoose(message);
            break;
        case 'directMessage':
            addMessage(message)
            break;
        case 'userList':
            userList(message)
            break;
        case 'webRTC-offer':
            webRTCConnection.setRemoteDescription(new RTCSessionDescription(message.offer));
            webRTCConnection.createAnswer().then(answer => {
                webRTCConnection.setLocalDescription(answer);
                socket.send(JSON.stringify({ 'messageType': 'webRTC-answer', 'answer': answer }));
            });
            break;
        case 'webRTC-answer':
            webRTCConnection.setRemoteDescription(new RTCSessionDescription(message.answer));
            break;
        case 'webRTC-candidate':
            webRTCConnection.addIceCandidate(new RTCIceCandidate(message.candidate));
            break;
        default:
            console.log("received an invalid WS messageType");
    }
}


function welcome() {

    get_chat_history()

    // use this line to start your video without having to click a button. Helpful for debugging
}