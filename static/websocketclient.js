// let username = "";
let playerTop = 0;
let playerLeft = 0;
let playerRadius = 0;

socket = new WebSocket('ws://' + window.location.host + '/gamews');
socket.addEventListener('message', (data)=>{

    // EACH TIME SOCKET WILL ASK FOR USER LOCATION
    // AND WILL RETURN TOTAL DATA FROM GAME

    const playerData = JSON.parse(data.data);
    // console.log("PlayerMap", playerData);
    userData = playerData["server_data"];
    // console.log("UserMap", userData);
    
    // username = playerData.id;
    if (userData.hasOwnProperty(username)){
        playerTop = userData[username]["location"][0]
        playerLeft = userData[username]["location"][1]
        playerRadius = userData[username]["size"]   
    }
    // Assuming userData is a Map
    for (let key in userData) {
        // console.log(key, userData[key]);
        addPlayer(key, userData[key]);
    }

    
    // Prepare data to send back
    const responseData = {
        message: "Hello from the server!",
        Username: username,
        user_data: {"location":[playerTop, playerLeft], "size":playerRadius}
    };

    socket.send(JSON.stringify(responseData));
})

function addPlayer(player, playerDict){
    const playerArea = document.getElementsByClassName("player-area");
    // console.log("PlayerArea",playerArea);
    // console.log("Inner Player", playerArea.innerHTML);
    Array.from(playerArea).forEach(pA => {
        // console.log("NEWPLAYERAREA",pA.innerHTML);
        const existingPlayer = pA.querySelector("#" + player); // Check if a player with the same id already exists
        console.log("ExistingPlayer",existingPlayer);
        if (existingPlayer) {
            // Player already exists, update specific values
            existingPlayer.style.left = 25;
            existingPlayer.style.top = 100;
            
        } else {
            // Player doesn't exist, add new player HTML
            pA.innerHTML += playerHTML(player, playerDict);
        }
    })
    // gameArea.innerHTML += playerHTML(player, playerDict);
}

function playerHTML(player, playerDict){
    let playerHTML = '<div id="' + player +'" style="left: '+ playerDict["location"][0] +'px; top: '+ playerDict["location"][1] +'px;">' + player + '</div>';
    return playerHTML;
}


document.addEventListener("DOMContentLoaded", function() {
    const gameArea = document.querySelector('.game-area');
    const player = document.getElementById(username);
    console.log("PLAYER",player)
    const playerRect = player.getBoundingClientRect();
    let playerCenterX = playerRect.left + playerRect.width / 2;
    let playerCenterY = playerRect.top + playerRect.height / 2;
    
    const playerRadius = Math.min(playerRect.width, playerRect.height) / 2;
    
    const baseSpeed = 200; // Base speed
    const speedMultiplier = 1 / playerRadius; // Speed multiplier
    
    document.addEventListener('keydown', function(e) {
        const keyW = 'w';
        const keyA = 'a';
        const keyS = 's';
        const keyD = 'd';
        
        let dx = 0;
        let dy = 0;
        
        if (e.key === keyW) {
            dy = -1; // Move up
        } else if (e.key === keyA) {
            dx = -1; // Move left
        } else if (e.key === keyS) {
            dy = 1; // Move down
        } else if (e.key === keyD) {
            dx = 1; // Move right
        }
        
        const magnitude = Math.sqrt(dx * dx + dy * dy);
        
        const normalizedDx = dx / magnitude;
        const normalizedDy = dy / magnitude;
        
        const speed = baseSpeed * speedMultiplier;
        
        // Calculate the potential new position
        const newPlayerCenterX = playerCenterX + normalizedDx * speed;
        const newPlayerCenterY = playerCenterY + normalizedDy * speed;
        
        // Check if the potential new position is within the boundaries
        const minX = 0;
        const minY = 0;
        const maxX = gameArea.offsetWidth - playerRect.width;
        const maxY = gameArea.offsetHeight - playerRect.height;
        
        if (newPlayerCenterX >= minX && newPlayerCenterX <= maxX &&
            newPlayerCenterY >= minY && newPlayerCenterY <= maxY) {
            playerCenterX = newPlayerCenterX;
            playerCenterY = newPlayerCenterY;
        }
        
        player.style.left = playerCenterX - playerRect.width / 2 + 'px';
        player.style.top = playerCenterY - playerRect.height / 2 + 'px';
        
    });
});
