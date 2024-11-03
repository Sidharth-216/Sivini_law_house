const socket = io.connect(window.location.origin);

const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
const muteMicButton = document.getElementById('muteMic');
const muteVideoButton = document.getElementById('muteVideo');
const endCallButton = document.getElementById('endCall');
const roomIdDisplay = document.getElementById('roomIdDisplay');
const loading = document.getElementById('loading');

let localStream;``
let peerConnection;
let micMuted = false;
let videoMuted = false;

// Retrieve room ID from URL
const urlParams = new URLSearchParams(window.location.search);
const roomId = urlParams.get('room'); 
roomIdDisplay.innerText = `Room ID: ${roomId}`; 

// Join the room using the room ID
socket.emit('join', { room: roomId });
loading.style.display = 'block';

// WebRTC configuration
const iceServers = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
        { urls: 'stun:stun1.l.google.com:19302' }
    ]
};

// Back button function
function goBack() {
    window.history.back();
}

// WebRTC connection setup
async function startCall() {
    try {
        // Request video and audio access
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localVideo.srcObject = localStream;

        peerConnection = new RTCPeerConnection(iceServers);

        peerConnection.onicecandidate = event => {
            if (event.candidate) {
                socket.emit('ice-candidate', { candidate: event.candidate, room: roomId });
            }
        };

        peerConnection.ontrack = event => {
            remoteVideo.srcObject = event.streams[0];
            loading.style.display = 'none'; // Hide loading message
        };

        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });

        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);
        socket.emit('offer', { offer: offer, room: roomId });

    } catch (error) {
        console.error("Error accessing media devices:", error);
        loading.style.display = 'none'; // Hide loading message
    }
}

// Mute/Unmute Microphone
muteMicButton.onclick = () => {
    micMuted = !micMuted;
    localStream.getAudioTracks()[0].enabled = !micMuted;
    muteMicButton.innerText = micMuted ? 'Unmute Mic' : 'Mute Mic';
};

// Mute/Unmute Video
muteVideoButton.onclick = () => {
    videoMuted = !videoMuted;
    localStream.getVideoTracks()[0].enabled = !videoMuted;
    muteVideoButton.innerText = videoMuted ? 'Unmute Video' : 'Mute Video';
};

// End Call
endCallButton.onclick = () => {
    localStream.getTracks().forEach(track => track.stop());
    peerConnection.close();
    socket.emit('end-call', { room: roomId });
    goBack(); // Redirect to previous page
};

// Offer/Answer exchange
socket.on('offer', async (offer) => {
    await peerConnection.setRemoteDescription(offer);
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);
    socket.emit('answer', { answer: answer, room: roomId });
});

socket.on('answer', async (answer) => {
    await peerConnection.setRemoteDescription(answer);
});

socket.on('ice-candidate', async (data) => {
    await peerConnection.addIceCandidate(data.candidate);
});

// Handle the end-call event
socket.on('end-call', () => {
    localStream.getTracks().forEach(track => track.stop());
    peerConnection.close();
    goBack(); // Redirect to previous page
});

// Start the call when the page loads
window.onload = startCall;
