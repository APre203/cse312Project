wss = false
let timerStarted = false
let socket = io();
if (wss){
    io.set('transports', ['websocket']);
    socket = io.connect("wss://heapoverflow312.me", { transports: ['websocket'] , upgrade: false });
}

// if (wss){
//     io.connect("https://heapoverflow312.me")
// }
async function initialize() {
    try {
        // Send request for game state
        // playerClear();
        socket.send("request-game-state", "get-game-state");

        
        const gameStatePromise = new Promise((resolve, reject) => {
            // Set up an event listener for the 'new-gamestate' event
            socket.on('new-gamestate', function(data) {
                // console.log("Received game state from server:", data);
                // Resolve the promise with the received game state data
                addPlayerstoDOM(data);
                // addUserListener();
                resolve(data);
                
            });
        });
        
        // Wait for the game state promise to resolve
        const gameStateData = await gameStatePromise;
        // console.log("Game state data received:", gameStateData);
        

    } catch (error) {
        console.error('Error initializing:', error);
    }
}

initialize();

// initialize();

// handleInit();
// socket.on('init', handleInit);

socket.on('new-gamestate', function(data){ // NEW GAMESTATE
    // console.log("Data From Server: ", data);
    playerClear();
    addPlayerstoDOM(data);
    // addUserListener();
   
});

socket.on('timer_started', function() {
    startTimer();
});

function startTimer() {
    if (!timerStarted) {
        socket.emit('start_timer');
        document.getElementById('start-timer-btn').style.display = 'none';
        document.getElementById('timer').style.display = 'block';
        timerStarted = true;
    }
  }

socket.on('update_timer', function(data) {
    // Extract the time remaining from the data received
    const timeRemaining = data.time;

    // Update the HTML element displaying the timer with the new time
    document.getElementById('time').textContent = timeRemaining + ' seconds';
});

function addPlayerstoDOM(gameStateData){
    for (let key in gameStateData) {
        // console.log(key, userData[key]);
        // if (key != username){
            addPlayer(key, gameStateData[key]);
        // }
    }
}

function playerHTML(player, playerDict){
    let playerHTML = '<div id="' + player +'" style="left: '+ playerDict["location"][1] +'px; top: '+ playerDict["location"][0] +'px;">' + player + '</div>';
    return playerHTML;
}

function playerClear(){
    const playerArea = document.getElementsByClassName("player-area");
    // console.log("PlayerArea",playerArea);
    // console.log("Inner Player", playerArea.innerHTML);
    Array.from(playerArea).forEach(pA => {
            pA.innerHTML = "";
        });
}

function addPlayer(player, playerDict){
    const playerArea = document.getElementsByClassName("player-area");
    // console.log("PlayerArea",playerArea);
    // console.log("Inner Player", playerArea.innerHTML);
    Array.from(playerArea).forEach(pA => {
        // console.log("NEWPLAYERAREA",pA.innerHTML);
        const existingPlayer = pA.querySelector("#" + player); // Check if a player with the same id already exists
        // console.log("ExistingPlayer",existingPlayer);
        if (existingPlayer) {
            // Player already exists, update specific values
            existingPlayer.style.left = playerDict["location"][1];
            existingPlayer.style.top = playerDict["location"][0];
            
        } else {
            // Player doesn't exist, add new player HTML
            pA.innerHTML += playerHTML(player, playerDict);
        }
    })
}

function sendUserData(){
    const player = document.getElementById(username);
    if (player != null){
        if (parseInt(player.style.top) != 0 || parseInt(player.style.left) != 0){
            socket.send("update-game-state", JSON.stringify({
                "username": {
                    "username": username,
                    "location": [parseInt(player.style.top), parseInt(player.style.left)],
                    "width": 10
                }
            }));
        }
    }
}

function updatePlayerLocation() {
    function movePlayer(dx, dy) {
        const player = document.getElementById(username);

        if (player != null){
            const playerRect = player.getBoundingClientRect();
            let playerLeft = playerRect.left;
            let playerTop = playerRect.top;

            const baseSpeed = 200; // Base speed
            const speedMultiplier = 0.25; // Speed multiplier (you can adjust this as needed)

            // Define the function to move the player
            
            const speed = baseSpeed * speedMultiplier;

            // Calculate the potential new position
            const newPlayerLeft = playerLeft + dx * speed;
            const newPlayerTop = playerTop + dy * speed;
            
            // Check if the potential new position is within the boundaries
            const minX = 10;
            const minY = 10;
            const maxX = window.innerWidth - playerRect.width - 10;
            const maxY = window.innerHeight - playerRect.height - 10;

            // Update the player's position within the boundaries
            playerLeft = Math.max(minX, Math.min(newPlayerLeft, maxX));
            playerTop = Math.max(minY, Math.min(newPlayerTop, maxY));

            // Set the new player position
            player.style.left = playerLeft + 'px';
            player.style.top = playerTop + 'px';
            }
        }

        // Add event listener for keydown events
        document.addEventListener('keydown', function(e) {
            let dx = 0;
            let dy = 0;

            // Determine the direction based on the pressed key
            if (e.key === 'w') {
                dy = -1; // Move up
            } else if (e.key === 'a') {
                dx = -1; // Move left
            } else if (e.key === 's') {
                dy = 1; // Move down
            } else if (e.key === 'd') {
                dx = 1; // Move right
            }

            // Move the player
            movePlayer(dx, dy);
            sendUserDataThrottled();
        });
}
let sendUserDataTimeout; 
function sendUserDataThrottled() {
    // Clear any existing timeout
    clearTimeout(sendUserDataTimeout);
    
    // Set a new timeout to send the user data after 250ms
    sendUserDataTimeout = setTimeout(sendUserData, 100);
}
updatePlayerLocation();
