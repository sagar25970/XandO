var context = {}

context.messagesScrolled = false

async function call(url='', method = 'GET', data = {}){
    if(method == 'GET'){
        var response = await fetch(url,
            {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }
    else if(method == 'POST'){
        var response = await fetch(url,
            {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
        )
    }
    return response.json()
}

function callPost(inputData){
    call('api-call', 'POST', inputData)
        .then(data => {
            parseData(data)
        }
    )
}

function callGet(){
    call('api-call', 'GET')
        .then(data => console.log(data))
}

function parseData(data){
    console.log(data)
    context.messages = data.messages
    var method_name = data.method_name
    var method_type = data.method_type

    if(method_name == "get-update"){
        let messages = data["messages"]
        document.getElementById("messages").innerHTML = ""
        messages.forEach(printMessage)
        scrollMessages()
        focusMessage()
    }
}

function printMessage(message){
    let username = message["username"]
    let data = message["data"]
    let chatMessage = document.createElement("div")
    chatMessage.classList.add("chat-box")
    console.log(context.username)
    console.log(username)
    if(context.username == username){
        chatMessage.classList.add("right")
        chatMessage.innerHTML = data
    } else{
        chatMessage.classList.add("left")
        chatMessage.innerHTML = username + " : " + data
    }
    document.body.appendChild(chatMessage)
    document.getElementById("messages").appendChild(chatMessage)
}

function scrollMessages(){
    if(!context.messagesScrolled){
        let messagesDiv = document.getElementById("messages")
        messagesDiv.scrollTop = messagesDiv.scrollHeight
    }
}

function focusMessage(){
    document.getElementById("message").focus()
}

setInterval(callPost, 3000)

/*
// Example POST method implementation:
async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

postData('https://example.com/answer', { answer: 42 })
  .then(data => {
    console.log(data); // JSON data parsed by `data.json()` call
  });
*/