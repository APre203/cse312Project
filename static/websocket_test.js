const socket = io();
handleInit();
socket.on('init', handleInit);

socket.on('new-gamestate', function(data){ // NEW GAMESTATE
    console.log("Data From Server: ", data);
});

function handleInit() {
    socket.send("request-game-state", "get-game-state")
    // await socket.on('new-gamestate', function(data){ // NEW GAMESTATE
    //     console.log("Data From Server: ", data);
    // });
    
}

socket.send("not-message", "in non message")