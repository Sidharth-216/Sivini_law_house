const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Serve static files
app.use(express.static(__dirname));

// Serve the main HTML file
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/call.html');
});

// Handle Socket.IO connections
io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('join', (data) => {
        console.log(`User joined room: ${data.room}`);
        socket.join(data.room);
    });

    socket.on('offer', (data) => {
        socket.to(data.room).emit('offer', data.offer);
    });

    socket.on('answer', (data) => {
        socket.to(data.room).emit('answer', data.answer);
    });

    socket.on('ice-candidate', (data) => {
        socket.to(data.room).emit('ice-candidate', data.candidate);
    });

    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

// Start the server
server.listen(3000, () => {
    console.log('Listening on port 3000');
});
