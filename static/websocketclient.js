let username = "";

socket = new WebSocket('ws://' + window.location.host + '/gamews');
socket.addEventListener('message', (data)=>{

    // EACH TIME SOCKET WILL ASK FOR USER LOCATION
    // AND WILL RETURN TOTAL DATA FROM GAME

    const playerData = JSON.parse(data.data);
    
    username = playerData.username;
    // // Log the received data
    console.log("PlayerMap", playerData);
    
    // // Prepare data to send back
    const responseData = {
        message: "Hello from the server!",
        Username: playerData.Username,
        message_inside_socket: playerData.message
    };

    socket.send(JSON.stringify(responseData));
})

// // https://www.youtube.com/watch?v=NVyeeZsYhF8