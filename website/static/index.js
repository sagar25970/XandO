var publicDict = {}

async function update(){
    const response = await fetch('update')

}

async function selectBox(url = '', data = {}){
    const response = await fetch(url)
    return response.json()
}

function select(box){
    selectBox('select-box/' + box.value, {})
    .then(x =>
            {
                console.log(x)
                document.getElementById('box' + box.value).innerHTML = 'X'
             }
    )
}

async function testUpdate(){
    const response = await fetch('testUpdate')
    response.json()
            .then(res => {
                    console.log(res)
                    res.message_data.forEach(displayMessage)
                    publicDict
                }
            )
}

function displayMessage(message){
    let newDiv = document.createElement("div")
    newDiv.innerHTML = message.player_id + ' ' + message.data
    document.getElementById('display').appendChild(newDiv)
}

setInterval(testUpdate, 3000)