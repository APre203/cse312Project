let username = "";

socket = new WebSocket('ws://' + window.location.host + '/gamews');
socket.addEventListener('message', (data)=>{

    // EACH TIME SOCKET WILL ASK FOR USER LOCATION
    // AND WILL RETURN TOTAL DATA FROM GAME

    const playerData = JSON.parse(data.data);
    console.log("PlayerMap", playerData);
    
    username = playerData.id;
    // Log the received data
    
    // Prepare data to send back
    const responseData = {
        message: "Hello from the server!",
        Username: username,
        message_inside_socket: playerData.server_data
    };

    socket.send(JSON.stringify(responseData));
})

// // https://www.youtube.com/watch?v=NVyeeZsYhF8