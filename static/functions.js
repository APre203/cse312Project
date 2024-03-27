function sendChat() {
    var messageInput = document.getElementById('chat-text-box');
    var message = messageInput.value.trim();
    if (message !== '') {
        // console.log("Message: ", message)
        // var username = 'User'; // You can retrieve username dynamically if you have user authentication
        var data1 = { "message":message };
        fetch('/chat/api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Content-Type-Options': 'nosniff'
            },
            body: JSON.stringify(data1)
        })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    // console.log("data",data)
                    addChatMessage(data,data1);
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

function addChatMessage(messageJSON,dat){
    // console.log("AddChat", messageJSON)
    var sidebar = document.getElementById('sidebar');
    var chatMessages = document.getElementById('chat-messages');
    var messageElement = document.createElement('div');
    var messageText = document.createElement('span');
    
    var likeButton = document.createElement('button');

    messageText.textContent = messageJSON.username + ': ' + messageJSON.message + ' ' +messageJSON.likes;
    
    likeButton.textContent = 'Like';
    likeButton.addEventListener('click', function() {
        // Handle like button click event
        fetch("/chat/getlikes",{
            body: JSON.stringify(dat)
        })
    .then(response => {
        // console.log(response)
        if (response.ok) {
            //clearChat();
            
            response.json().then(data => {
                console.log(data)
                // for (const message of data){
                //     addChatMessage(message);
                // }
                }
                ) // Will be a list of maps with username and message as key
            // const messages = JSON.parse(response);
            // console.log(messages)
        } else {
            throw new Error('Failed to get chat message');
        }
        //updateChat()
    })
    .catch(error => {
        console.error(error);
        // Handle error
    });
        console.log('Like button clicked for message:', messageJSON.message);
       // updateChat()
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

setInterval(updateChat, 5000);