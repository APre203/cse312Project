wss = false
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
                const players = data.players;
                const balls = data.balls;
                const leaders = data.leaders;
                // console.log("players",players)
                // console.log("balls",balls)
                addPlayerstoDOM(players);
                addBallstoDOM(balls);
                addLeaderstoDOM(leaders);
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
    const players = data.players;
    const balls = data.balls;
    const leaders = data.leaders;
    // console.log("players",players)
    // console.log("balls",balls)
    playerClear();
    ballsClear();
    leaderClear();
    addPlayerstoDOM(players);
    addBallstoDOM(balls);
    addLeaderstoDOM(leaders);
    // addUserListener();
   
});

function addPlayerstoDOM(gameStateData){
    for (let key in gameStateData) {
        // console.log(key, userData[key]);
        // if (key != username){
            addPlayer(key, gameStateData[key]);
        // }
    }
}

function addBallstoDOM(balls){
    for (let b in balls){
        // console.log("B", b)
        const ball = balls[b]
        addBalls(ball[0],ball[1]);
    }
}

function addBalls(top, left){
    const playerArea = document.getElementsByClassName("balls-location");
    // console.log("PlayerArea",playerArea);
    // console.log("Inner Player", playerArea.innerHTML);
    Array.from(playerArea).forEach(pA => {
        pA.innerHTML += ballHTML(top, left);
    })
}

function ballHTML(top, left){
    // console.log("HTML top - left",top, left)
    let ballHTML = '<div class="' + "balls" +'" style="left: '+ left +'px; top: '+ top +'px;"></div>';
    return ballHTML;
}

function ballsClear(){
    const playerArea = document.getElementsByClassName("balls-location");
    // console.log("PlayerArea",playerArea);
    // console.log("Inner Player", playerArea.innerHTML);
    Array.from(playerArea).forEach(pA => {
            pA.innerHTML = "";
        });
}

function addLeaderstoDOM(leaders){
    for (let b in leaders){
        // console.log("B", b)
        const leader = leaders[b]
        addLeaders(leader[0],leader[1]); // name, score
    }
}

function addLeaders(name, score){
    const leaderboard = document.getElementsByClassName("leaderboard");
    // console.log("PlayerArea",playerArea);
    // console.log("Inner Player", playerArea.innerHTML);
    Array.from(leaderboard).forEach(pA => {
        pA.innerHTML += leaderHTML(name, score);
    })
}

function leaderHTML(name, score){
    let playerHTML = '<div>' + name + " : " + score + '</div>';
    return playerHTML;
}

function leaderClear(){
    const leaderboard = document.getElementsByClassName("leaderboard")[0];
    leaderboard.innerHTML = "";
}


function playerHTML(player, playerDict){
    let playerHTML = '<div class="players" id="' + player +'" style="left: '+ playerDict["location"][1] +'px; top: '+ playerDict["location"][0] +'px;">' + player + '</div>';
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
        // console.log(player, playerDict.score)
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

let ballsFound = [];
let userScore = 0;
function sendUserData(){
    const player = document.getElementById(username);
    if (player != null){
        if (parseInt(player.style.top) != 0 || parseInt(player.style.left) != 0){
            socket.send("update-game-state", JSON.stringify({
                "username": {
                    "username": username,
                    "location": [parseInt(player.style.top), parseInt(player.style.left)],
                    "width": 10,
                    "score":userScore
                },
                "balls":ballsFound
            }));
            ballsFound = [];
            userScore = 0;
        }
    }
}


function findBallsNear() {
    const playerArea = document.getElementsByClassName("player-area")[0];
    const existingPlayer = playerArea.querySelector("#" + username);
    const ballsLocation = document.getElementsByClassName('balls-location')[0];

    if (existingPlayer) {
        // Get the bounding rectangle of the player
        const playerRect = existingPlayer.getBoundingClientRect();

        // Get all ball elements within the ballsLocation container
        const balls = ballsLocation.querySelectorAll('.balls');

        // Loop through each ball
        balls.forEach(ball => {
            // Get the bounding rectangle of the current ball
            const ballRect = ball.getBoundingClientRect();

            // Calculate the distance between the player and the ball
            const distance = Math.sqrt(Math.pow(playerRect.x - ballRect.x, 2) + Math.pow(playerRect.y - ballRect.y, 2));

            // Log the distance for testing purposes
            if (distance <= 35){
                // console.log("Distance between player and ball: " + distance);
                ballsFound.push([ballRect.top,ballRect.left]);
                // increase score by 1
                userScore+=1;
                ball.remove();
            }
        });
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

            findBallsNear();

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
