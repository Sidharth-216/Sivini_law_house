const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const PORT = 3000;

// Serve static files
app.use(express.static(path.join(__dirname, "static")));

// Room management
const rooms = {};

io.on("connection", (socket) => {
    console.log("A user connected:", socket.id);

    // Create a room
    socket.on("create", (roomId) => {
        if (!rooms[roomId]) {
            rooms[roomId] = [];
        }
        rooms[roomId].push(socket.id);
        socket.join(roomId);
        console.log(`Room created: ${roomId}`);
    });

    // Join a room
    socket.on("join", (roomId) => {
        if (rooms[roomId]) {
            socket.join(roomId);
            rooms[roomId].push(socket.id);
            console.log(`User ${socket.id} joined room: ${roomId}`);

            // Notify other members in the room
            socket.to(roomId).emit("ready");
        } else {
            socket.emit("error", "Room does not exist");
            console.log(`Attempt to join non-existent room: ${roomId}`);
        }
    });

    // Handle WebRTC offer
    socket.on("offer", (data) => {
        const { roomId, offer } = data;
        socket.to(roomId).emit("offer", offer);
        console.log(`Offer sent to room: ${roomId}`);
    });

    // Handle WebRTC answer
    socket.on("answer", (data) => {
        const { roomId, answer } = data;
        socket.to(roomId).emit("answer", answer);
        console.log(`Answer sent to room: ${roomId}`);
    });

    // Handle ICE candidates
    socket.on("candidate", (data) => {
        const { roomId, candidate } = data;
        socket.to(roomId).emit("candidate", candidate);
        console.log(`ICE candidate sent to room: ${roomId}`);
    });

    // Handle user disconnect
    socket.on("disconnect", () => {
        console.log("User disconnected:", socket.id);

        for (const roomId in rooms) {
            rooms[roomId] = rooms[roomId].filter((id) => id !== socket.id);
            if (rooms[roomId].length === 0) {
                delete rooms[roomId];
                console.log(`Room deleted: ${roomId}`);
            }
        }
    });
});

// Run the server
server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${5001}`);
});
