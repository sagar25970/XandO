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

function test(){
    callGet('test-api')
}

function db(){
    callGet('db')
}