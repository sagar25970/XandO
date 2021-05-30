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

function callPost(url, inputData=""){
    call(url, 'POST', inputData)
        .then(data => {
            parseData(data)
        }
    )
}

function callGet(url){
    call(url, 'GET')
        .then(data => console.log(data))
}

function callUpdate(){
    callPost('update')
}

function parseData(data){
    console.log(data)
    context.messages = data.messages
    var method_name = data.method_name
    var method_type = data.method_type

    if(method_name == "get_update"){
        let messages = data.messages
        let game = data.game
        let game_state = game.game_state
        document.getElementById("messages").innerHTML = ""
        messages.forEach(printMessage)
        scrollMessages()
        focusMessage()
        updateGame(game_state)
    } else if(method_name == "select_box"){
        updateGame(data.game.game_state)
    }
}

function updateGame(game_state){
    for(let i = 0; i<9; i++){
        document.getElementById("box" + i).innerHTML = game_state.charAt(i)
    }
}

function printMessage(message){
    let username = message["username"]
    let data = message["data"]
    let chatMessage = document.createElement("div")
    chatMessage.classList.add("chat-box")
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

function selectBox(box){
    callPost("/select-box/" + box.value)
}

function reset(){
    callGet('reset')
}

setInterval(callUpdate, 3000)

/*
// Example POST method implementation:
async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PgameUT, DELETE, etc.
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