document.addEventListener("DOMContentLoaded", function() {
  return 0  
  const gameArea = document.querySelector('.game-area');
    const player = document.getElementById('player');
    const playerRect = player.getBoundingClientRect();
    let playerCenterX = playerRect.left + playerRect.width / 2;
    let playerCenterY = playerRect.top + playerRect.height / 2;
    
    let mouseX = playerCenterX;
    let mouseY = playerCenterY;
    
    const speed = 2; // Adjust this value to change the speed of the player
    
    document.addEventListener('mousemove', function(e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });
    
    const update = () => {
      let dx = mouseX - playerCenterX;
      let dy = mouseY - playerCenterY;
    
      // console.log(dx, dy)
      

      if (dy < 0) {
          dy = -1; // Move up
      } else if (dy > 0) {
        dy = 1; // Move down
      } 
      if (dx < 0) {
          dx = -1; // Move left
      }else if (dx > 0) {
          dx = 1; // Move right
        }

    
    
      const distance = Math.sqrt(dx * dx + dy * dy);
      

      const normalizedDx = dx ;
      const normalizedDy = dy ;
      

      if (distance > 0) {
        const ratio = speed / distance;
        
        // playerCenterX += moveX;
        // playerCenterY += moveY;

        playerCenterX += normalizedDx * speed ;
        playerCenterY += normalizedDy * speed ;
      
        
        // Update the position of the player object
        player.style.left = playerCenterX - playerRect.width / 2 + 'px';
        player.style.top = playerCenterY - playerRect.height / 2 + 'px';
        
        // Update the position of the game area to create the illusion of movement
        const offsetX = gameArea.offsetWidth / 2 - playerCenterX;
        const offsetY = gameArea.offsetHeight / 2 - playerCenterY;
        gameArea.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
      }
      
      requestAnimationFrame(update);
    };
    
    update();
});



document.addEventListener("DOMContentLoaded", function() {
  return 0  
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
        
        playerCenterX += normalizedDx * speed;
        playerCenterY += normalizedDy * speed;
        
        player.style.left = playerCenterX - playerRect.width / 2 + 'px';
        player.style.top = playerCenterY - playerRect.height / 2 + 'px';
        
        const offsetX = gameArea.offsetWidth / 2 - playerCenterX;
        const offsetY = gameArea.offsetHeight / 2 - playerCenterY;
        gameArea.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
    });
});
