async function storeDatabase(message, token, sendto){
    let msg_body = {
        msg : message,
        dest : sendto
    };
    let response = await fetch('/home/store/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : token
        },
        body: JSON.stringify(msg_body)
    })
    return await response.json()
}

async function send(){
    let sendto = $("#user-name")
    let chat = $("#chat")
    let username = $("#username")
    let csrftoken  = $('input[name=csrfmiddlewaretoken]')
    if($.trim(chat.val()) != ''){
        let msg = chat.val()
        
        let flex_msg = $("<div class='p-2 bg-primary rounded-pill text-light'></div>").text(chat.val())
        let flex_username = $("<span class='d-flex justify-content-end px-1'></span>").text(username.val())
        let dflex = $("<div class='d-flex justify-content-end mb-3'></div>").append(flex_msg)
        flex_username.appendTo('#chat-field')
        dflex.appendTo('#chat-field')
        chat.val('')
        $("#chat-field").animate({scrollTop: $(document).height()}, 500)

        let message = JSON.stringify({message : msg, dest: sendto.val()})
        await storeDatabase(msg, csrftoken.val(), sendto.val())
        await socket.send(message)
    }
}

$("#send").click(function(){
    send()
});

$("#chat").keypress(function(event){
    if(event.keyCode == 13)
        send()
});