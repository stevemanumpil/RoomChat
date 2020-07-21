const socket = new WebSocket("ws://127.0.0.1:5575");
$(function(){
    let idle = '';
//   setInterval(update, 500);
//
//    $("#send").click(function(){
//        let chat = $("#chat").val()
//        let csrftoken  = $('input[name=csrfmiddlewaretoken]').val()
//
//        $.ajax({
//            url: '/home/req/',
//            type: "post",
//            dataType: 'json',
//            data : {
//                chat : chat,
//                csrfmiddlewaretoken : csrftoken
//            },
//            success: function(data){
//                console.log(data)
//                //$("#chat-field").append("<span class='badge badge-pill badge-secondary py-2 px-2 my-1' style='font-size: 15px'>"+data+"</span><br>")
//                $("#chat").val('')
//            }
//        })
//    })
//
//    function update(){
//        $.ajax({
//            url : '/home/get_message/',
//            type: 'get',
//            dataType : 'json',
//            success: function(data) {
//                if(data != 'empty' && data != 'blom'){
//                    $("#chat-field").append("<span class='badge badge-pill badge-secondary py-2 px-2 my-1' style='font-size: 15px'>"+data+"</span><br>")
//                }
//            }
//        });
//    }

    function connect(){
        socket.addEventListener('open', (event) => {
            console.log("successfully conected");
            let message = {
                username : $("#username").val(),
                id : $("#id").val()
            }
            message = JSON.stringify(message)
            socket.send(message)
        });

        socket.addEventListener('message', (event) => {
            console.log("there's a message for you");
            let new_msg = JSON.parse(event.data);
            if(idle == new_msg.username){
                let flex_msg = $("<div class='p-2 bg-primary rounded-pill text-light'></div>").text(new_msg.message);
                let flex_username = $("<span class='d-flex justify-content-start px-1'></span>").text(new_msg.username);
                let dflex = $("<div class='d-flex justify-content-start mb-3'></div>").append(flex_msg);
                flex_username.appendTo('#chat-field');
                dflex.appendTo('#chat-field');
                $("#chat-field").animate({scrollTop: $(document).height()}, 500)
            }
            else{
                let notif_sound = new Audio('/static/dashboard/media/chat.mp3');
                notif_sound.play();
                let val = $("[data-user="+new_msg.username+"]").find(".notif");
                let jml = parseInt(val.text());
                jml++;
                val.text(jml);
                val.removeClass("sr-only");
            }
        });

        socket.addEventListener('error', (event) => {
            console.log('something error')
        });

        socket.addEventListener('close', (event) => {
            console.log('connection close')
        });
    }

    async function loadPanel(username){
        let parser = new DOMParser()
        let req_msg = await fetch('/home/load/'+username)
        let msg = await req_msg.json()
        msg = msg.response

        let req_panel = await fetch('/home/panel/'+username)
        let doc = parser.parseFromString(await req_panel.text(),'text/html')
        let chat_field = doc.getElementById("chat-field")

        if(Array.isArray(msg)){
            for(pr in msg){
                let flex_msg = $("<div class='p-2 bg-primary rounded-pill text-light'></div>").text(msg[pr].text)
                let flex_username = $("<span class='d-flex justify-content-"+msg[pr].position+" px-1'></span>").text(msg[pr].user)
                let dflex = $("<div class='d-flex justify-content-"+msg[pr].position+" mb-3'></div>").append(flex_msg)
                flex_username.appendTo(chat_field)
                dflex.appendTo(chat_field)
            }
        }
        $("main").html(doc.body.children)
        $.getScript('/static/dashboard/js/send.js')
        chat_field.scrollTop = chat_field.scrollHeight
    }   

    
    $("#logout").click(function(event){
        event.preventDefault()
         let message = {
            quit : 'disconnect'
         };
         message = JSON.stringify(message)
         socket.send(message)
         location.replace('/home/logout')
    });

    $("a.list-group-item").on('click', function(event){
        event.preventDefault();
        let username = $(this).find('span.font-weight-bold').text();
        $(this).find(".notif").addClass("sr-only");
        $(this).find(".notif").text(0);
        idle = username;
        loadPanel(username);
    
    //    $.ajax({
    //        url : '/home/req/'+userid+'/',
    //        type : 'GET',
    //        dataType: 'html',
    //        success: function(data){
    //            $("main").html(data)
    //            $.getScript('/static/dashboard/js/send.js')
    //        }
    //    })
    })

    $("#group").click(function(){
        
    });

    connect();
})

