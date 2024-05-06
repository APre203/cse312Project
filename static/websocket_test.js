wss = false
const socket = io.connect("http://" + document.domain + ":" + location.port);
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
                resolve(data);
                // addUserListener()
                
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

function addPlayerstoDOM(gameStateData){
    for (let key in gameStateData) {
        // console.log(key, userData[key]);
        if (key != "null"){
            addPlayer(key, gameStateData[key]);
        }
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
            
            if (player != username && existingPlayer.style.left != playerDict["location"][1] && existingPlayer.style.top != playerDict["location"][0] ){
                console.log("changing position", player)
                existingPlayer.style.left = playerDict["location"][1];
                existingPlayer.style.top = playerDict["location"][0];
                // notcheckedPlayer[player] = false
            }
        
            
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

function updatePlayerLocationMOUSE() { // mouse movement
    function movePlayerTowardsMouse(mouseX, mouseY) {

        const player = document.getElementById(username);
        if (player != null) {
            console.log("here")
            const playerRect = player.getBoundingClientRect();
            const playerLeft = playerRect.left;
            const playerTop = playerRect.top;

            const baseSpeed = 5; // Base speed
            const speedMultiplier = 1; // Speed multiplier

            // Calculate the direction towards the mouse cursor
            const dx = mouseX - (playerLeft + playerRect.width / 2);
            const dy = mouseY - (playerTop + playerRect.height / 2);

            // Calculate the magnitude (distance) between the player and mouse cursor
            const distance = Math.sqrt(dx * dx + dy * dy);

            // Normalize the direction vector
            const normalizedDx = dx / distance;
            const normalizedDy = dy / distance;

            // Calculate the movement distance based on the speed
            const movementX = normalizedDx * baseSpeed * speedMultiplier;
            const movementY = normalizedDy * baseSpeed * speedMultiplier;

            // Calculate the new player position
            let newPlayerLeft = playerLeft + movementX;
            let newPlayerTop = playerTop + movementY;

            // Ensure the player stays within certain bounds
            const minX = 10;
            const minY = 10;
            const maxX = window.innerWidth - playerRect.width - 10;
            const maxY = window.innerHeight - playerRect.height - 10;

            newPlayerLeft = Math.max(minX, Math.min(newPlayerLeft, maxX));
            newPlayerTop = Math.max(minY, Math.min(newPlayerTop, maxY));

            // Set the new player position
            player.style.left = newPlayerLeft + 'px';
            player.style.top = newPlayerTop + 'px';
            }
        }
        // Add mousemove event listener to the document
        document.addEventListener('mousemove', function(e) {
            const mouseX = e.clientX;
            const mouseY = e.clientY;

            let dx = mouseX;
            let dy = mouseY;

            // Move the player
            movePlayerTowardsMouse(dx, dy);
            sendUserDataThrottled();
        });
    
}

// Call the function to start updating player location
updatePlayerLocation();


// setInterval(sendUserData, 250)