// Connect to the socket.io server
const socket = io.connect();

// UI Elements
const createRoomBtn = document.getElementById('createRoomBtn');
const joinRoomBtn = document.getElementById('joinRoomBtn');
const roomIdDisplay = document.getElementById('roomIdDisplay');
const roomIdInput = document.getElementById('roomIdInput');
const videoChat = document.getElementById('video-chat');
const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
const muteAudioBtn = document.getElementById('muteAudioBtn');
const muteVideoBtn = document.getElementById('muteVideoBtn');
const endCallBtn = document.getElementById('endCallBtn');
const nameInput = document.getElementById('nameInput'); // Name input field

// Media stream variables
let localStream;
let remoteStream;
let peerConnection;
let roomId;
let userName;

// Setting up the media devices (camera and microphone)
navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        localStream = stream;
        localVideo.srcObject = stream;
    })
    .catch(err => console.log("Error accessing media devices: " + err));

// Create Room: Generate and display a unique Room ID
createRoomBtn.addEventListener('click', () => {
    roomId = 'room_' + Math.floor(Math.random() * 10000);  // Random room ID
    roomIdDisplay.textContent = `Room ID: ${roomId}`;
    socket.emit('create_room', roomId);  // Notify server to create the room
    videoChat.style.display = 'block';   // Show the video chat UI
    createRoomBtn.disabled = true;      // Disable the "Create Room" button
    joinRoomBtn.disabled = true;        // Disable the "Join Room" button
});

// Join Room: Enter an existing Room ID
joinRoomBtn.addEventListener('click', () => {
    roomId = roomIdInput.value;  // Get the Room ID from input
    userName = nameInput.value;  // Get the user's name

    if (roomId && userName) {
        socket.emit('join_room', roomId, userName);  // Notify server to join the room with the user name
        videoChat.style.display = 'block';  // Show the video chat UI
    } else {
        alert('Please enter a valid Room ID and your Name');
    }
});

// Socket event when the room is created
socket.on('room_created', (roomId) => {
    console.log(`Room ${roomId} created successfully.`);
});

// Socket event when the room is joined
socket.on('room_joined', (roomId, userName) => {
    console.log(`Joined room: ${roomId}`);
    startPeerConnection(roomId);  // Start peer connection when room is joined
    alert(`${userName} has joined the room.`);
});

// Socket event for a new participant joining the room
socket.on('new_participant', (userName) => {
    console.log(`${userName} has joined the room.`);
});

// Start peer connection for video call
function startPeerConnection(roomId) {
    const configuration = {
        iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    };
    peerConnection = new RTCPeerConnection(configuration);

    // Add local stream to the peer connection
    localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

    // Create an offer if you're the first one in the room (host)
    peerConnection.createOffer()
        .then(offer => peerConnection.setLocalDescription(offer))
        .then(() => socket.emit('offer', roomId, peerConnection.localDescription));

    // Handle incoming ICE candidates
    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            socket.emit('candidate', roomId, event.candidate);
        }
    };

    // Handle remote stream when the remote participant streams video/audio
    peerConnection.ontrack = (event) => {
        if (!remoteStream) {
            remoteStream = event.streams[0];
            remoteVideo.srcObject = remoteStream;
        }
    };
}

// Mute/Unmute Audio
muteAudioBtn.addEventListener('click', () => {
    let audioTrack = localStream.getAudioTracks()[0];
    audioTrack.enabled = !audioTrack.enabled;
    muteAudioBtn.textContent = audioTrack.enabled ? 'Mute Audio' : 'Unmute Audio';
});

// Mute/Unmute Video
muteVideoBtn.addEventListener('click', () => {
    let videoTrack = localStream.getVideoTracks()[0];
    videoTrack.enabled = !videoTrack.enabled;
    muteVideoBtn.textContent = videoTrack.enabled ? 'Mute Video' : 'Unmute Video';
});

// End the Call
endCallBtn.addEventListener('click', () => {
    socket.emit('end_call', roomId);
    peerConnection.close();
    videoChat.style.display = 'none';
    createRoomBtn.disabled = false;
    joinRoomBtn.disabled = false;
});

// Receive ICE candidate from server
socket.on('candidate', (candidate, roomId) => {
    peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
});

// Receive the offer from other peer (for clients joining the room)
socket.on('offer', (roomId, offer) => {
    peerConnection.setRemoteDescription(new RTCSessionDescription(offer))
        .then(() => peerConnection.createAnswer())
        .then(answer => peerConnection.setLocalDescription(answer))
        .then(() => socket.emit('answer', roomId, peerConnection.localDescription));
});

// Receive the answer from other peer
socket.on('answer', (roomId, answer) => {
    peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
});
