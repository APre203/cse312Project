document.addEventListener("DOMContentLoaded", function() {
    const gameArea = document.querySelector('.game-area');
    const player = document.getElementById('player');
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
