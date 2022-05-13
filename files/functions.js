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
    const userBox = document.getElementById("dm-user");
    const recipient = userBox.value;
    chatBox.value = "";
    chatBox.focus();
    if (comment !== "") {
        socket.send(JSON.stringify({ 'messageType': 'chatMessage', 'comment': comment, 'recipient': recipient }));
    }
}

function upGooseMessage(id) {
    if (id !== "") {
        socket.send(JSON.stringify({ 'messageType': 'upGoose', 'id': id }));
    }
}

// Renders a new chat message to the page
function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    if (chatMessage["recipient"] == "all") {
        chat.innerHTML = "<b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<button onclick='upGooseMessage(\"" + chatMessage["id"] + "\")'> UpGoose! </button><div id='" + chatMessage["id"] + "'>" + chatMessage["ups"].length + "</div><br/>" + chat.innerHTML;
    } else {
        chat.innerHTML = "<b>DM: " + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<button onclick='upGooseMessage(\"" + chatMessage["id"] + "\")'> UpGoose! </button><div id='" + chatMessage["id"] + "'>" + chatMessage["ups"].length + "</div><br/>" + chat.innerHTML;
    }
}

function upGoose(message) {
    let upGooseMessage = document.getElementById(message)
    console.log(upGooseMessage)
    upGooseMessage.innerHTML = parseInt(upGooseMessage.innerHTML) + 1
}

function userList(message) {
    let users = document.getElementById('users');
    users.innerHTML = "";
    console.log(message);
    console.log(Object.entries(message["users"]));
    for (var [user, stuff] of Object.entries(message["users"])) {
        users.innerHTML += "<div class=\"username\">";
        users.innerHTML += "<b>" + user + "</b> " + "<br/>";
        users.innerHTML += "<img class=\"profileimg\" src=\"" + stuff + "\"></div><br/>"
    }
    if (users.innerHTML === "") {
        users.innerHTML = "<h3>No users online currently!</h3>"
    }
    let userSelect = document.getElementById("dm-user");
    userSelect.innerHTML = "<option value='all'>All</option>"
    for (var [user, stuff] of Object.entries(message["users"])) {
        userSelect.innerHTML += "<option value='" + user + "'>" + user + "</option>"
    }

    function upGoose(message) {
        let upGooseMessage = document.getElementById(message)
        console.log(upGooseMessage)
        upGooseMessage.innerHTML = parseInt(upGooseMessage.innerHTML) + 1
    }
}

// called when the page loads to get the chat_history
function get_chat_history() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);
            for (const message of messages) {
                message["id"] = message["_id"]["$oid"]
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
            upGoose(message["id"]);
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
