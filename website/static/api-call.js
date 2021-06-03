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
        document.getElementById("messages").innerHTML = ""
        messages.forEach(printMessage)
        scrollMessages()
        focusMessage()
        updateGame(game)
    } else if(method_name == "select_box" && data.status == '200'){
        updateGame(data.game)
    }
}

function updateGame(game){
    var disableBox = false;
    if(context.username != game.current_turn || !game.current_o || game.game_won){
        var disableBox = true;
    }
    for(let i = 0; i<9; i++){
        document.getElementById("box" + i).innerHTML = game.game_state.charAt(i)
        document.getElementById("box" + i).disabled = disableBox
    }

    var disablePlayer = true
    if(game.current_x == null && context.username != game.current_o){
        disablePlayer = false
    }
    document.getElementById("player1").disabled = disablePlayer
    disablePlayer = true
    if(!game.current_o && context.username != game.current_x){
        disablePlayer = false
    }
    document.getElementById("player2").disabled = disablePlayer
    if(game.current_x){
        document.getElementById("x-name").innerHTML = 'X : ' +  game.current_x
    } else {
        document.getElementById("x-name").innerHTML = ''
    }
    if(game.current_o){
        document.getElementById("o-name").innerHTML = 'O : ' + game.current_o
    } else{
        document.getElementById("o-name").innerHTML = ''
    }

    if(game.game_won){
        document.getElementById("winner").innerHTML = 'Winner : ' + game.game_won
    } else{
        document.getElementById("winner").innerHTML = ''
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

function player1(){
    callPost('player1')
}

function player2(){
    callPost('player2')
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