function sendChat() {
    var messageInput = document.getElementById('chat-text-box');
    var message = messageInput.value.trim();
    if (message !== '') {
        // console.log("Message: ", message)
        // var username = 'User'; // You can retrieve username dynamically if you have user authentication
        var data = { "message":message };
        fetch('/chat/api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Content-Type-Options': 'nosniff'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    // console.log("data",data)
                    addChatMessage(data);
                    messageInput.value = ''; // Clear the input box after sending
                })
            } else {
                throw new Error('Failed to send chat message');
            }
        })
        .catch(error => {
            console.error(error);
            // Handle error
        });
    }
}


function addChatMessage(messageJSON) {
    var sidebar = document.getElementById('sidebar');
    var chatMessages = document.getElementById('chat-messages');
    var messageElement = document.createElement('div');
    var messageText = document.createElement('span');

    var likeButton = document.createElement('button');
    likeButton.className = 'like-button';
    likeButton.innerHTML = '<i class="fas fa-thumbs-up"></i><span class="like-count">0</span>';
    
    messageText.textContent = messageJSON.username + ': ' + messageJSON.message;

    likeButton.addEventListener('click', function() {
        // Handle like button click event
        // Increment like count
        var likeCountSpan = this.querySelector('.like-count');
        var currentCount = parseInt(likeCountSpan.textContent);
        likeCountSpan.textContent = currentCount + 1;
    });

    messageElement.appendChild(messageText);
    messageElement.appendChild(likeButton);
    chatMessages.insertBefore(messageElement, chatMessages.firstChild);
    sidebar.scrollTop = 0; // Scroll to top to show the latest message
}

function clearChat() {
    var chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = "";
}

function updateChat(){
    fetch("/chat/api")
    .then(response => {
        // console.log(response)
        if (response.ok) {
            clearChat();
            
            response.json().then(data => {
                // console.log(data)
                for (const message of data){
                    addChatMessage(message);
                }
                }
                ) // Will be a list of maps with username and message as key
            // const messages = JSON.parse(response);
            // console.log(messages)
        } else {
            throw new Error('Failed to get chat message');
        }
    })
    .catch(error => {
        console.error(error);
        // Handle error
    });

}

function likeButton() {

    fetch('/chat/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Content-Type-Options': 'nosniff'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            response.json().then(data => {
                // console.log("data",data)
                addChatMessage(data);
                messageInput.value = ''; // Clear the input box after sending
            })
        } else {
            throw new Error('Failed to send chat message');
        }
    })
    .catch(error => {
        console.error(error);
        // Handle error
    });

    const likeButton = document.getElementById('like-button');
    const likeCountElement = document.getElementById('like-count');
    let likeCount = parseInt(likeCountElement.innerText);

    if (likeButton.classList.contains('liked')) {
        // If already liked, unlike it
        likeCount--;
        likeButton.classList.remove('liked');
    } else {
        // If not liked, like it
        likeCount++;
        likeButton.classList.add('liked');
    }

    likeCountElement.innerText = likeCount;
}


setInterval(updateChat, 5000);