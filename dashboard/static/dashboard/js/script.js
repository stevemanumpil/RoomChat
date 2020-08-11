$(function(){
    const socket = new WebSocket("ws://127.0.0.1:5575");
    let part_send = '';
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
                username : $("#user-login").text(),
                id : $("#id").text()
            }
            message = JSON.stringify(message)
            socket.send(message)
        });

        socket.addEventListener('message', (event) => {
            console.log("there's a message for you");
            let new_msg = JSON.parse(event.data);
            if(idle == new_msg.room){
                let flex_msg = $("<div class='p-2 bg-primary rounded-pill text-light'></div>").text(new_msg.message);
                let flex_username = $("<span class='d-flex justify-content-start px-1'></span>").text(new_msg.sender);
                let dflex = $("<div class='d-flex justify-content-start mb-3'></div>").append(flex_msg);
                flex_username.appendTo('#chat-field');
                dflex.appendTo('#chat-field');
                $("#chat-field").animate({scrollTop: $(document).height()}, 500)
            }
            else{
                let notif_sound = new Audio('/static/dashboard/media/chat.mp3');
                notif_sound.play();
                let val = $("[data-room='"+new_msg.room+"']").find(".notif");
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

    async function loadMessage(room_name){
        let req_msg = await fetch('/home/load/'+room_name)
        let msg = await req_msg.json()
        let chat_field = document.getElementById('chat-field')
        chat_field.innerHTML = ''
        part_send = msg.participant

        if(Array.isArray(msg.response)){
            for(pr in msg.response){
                let flex_msg = $("<div class='p-2 bg-primary rounded-pill text-light'></div>").text(msg.response[pr].text)
                let flex_username = $("<span class='d-flex justify-content-"+msg.response[pr].position+" px-1'></span>").text(msg.response[pr].user)
                let dflex = $("<div class='d-flex justify-content-"+msg.response[pr].position+" mb-3'></div>").append(flex_msg)
                flex_username.appendTo(chat_field)
                dflex.appendTo(chat_field)
            }
        }
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

    // $("a.list-group-item").on('click', function(event){
    //     event.preventDefault();
    //     let username = $(this).find('.username').text()
    //     let room_name = $(this).data('room');
    //     $(this).find(".notif").addClass("sr-only");
    //     $(this).find(".notif").text(0);
    //     $("#chat").val('')
    //     idle = room_name
    //     $("#panel #panel_name").text(username)
    //     $(this).tab('show');

    //     loadMessage(room_name)
    // })

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
        let sendto = idle
        let chat = $("#chat")
        let user_login = $("#user-login")
        let csrftoken  = $('input[name=csrfmiddlewaretoken]')
        if($.trim(chat.val()) != ''){
            let msg = chat.val()

            let flex_msg = $("<div class='p-2 bg-primary rounded-pill text-light'></div>").text(chat.val())
            let flex_username = $("<span class='d-flex justify-content-end px-1'></span>").text(user_login.text())
            let dflex = $("<div class='d-flex justify-content-end mb-3'></div>").append(flex_msg)
            flex_username.appendTo('#chat-field')
            dflex.appendTo('#chat-field')
            chat.val('')
            $("#chat-field").animate({scrollTop: $(document).height()}, 500)
            
            await storeDatabase(msg, csrftoken.val(), sendto)

            for(pr in part_send){
                let message = JSON.stringify({message : msg, dest: part_send[pr].username, room: idle})
                await socket.send(message)
            }
        }
    }

    async function checkRoomChat(msg){
        let panel = await fetch('/home/check/', {
            method : 'POST',
            headers : {
                'Content-type' : 'application/json',
                'X-CSRFToken' : $('input[name=csrfmiddlewaretoken]').val()
            },
            body : JSON.stringify(msg)
        })
    }
    
    $("#send").click(function(){
        send()
    });
    
    $("#chat").keypress(function(event){
        if(event.keyCode == 13)
            send()
    });

    $(".nav-pills a").click(function(event){
        event.preventDefault()
        $(this).tab('show')
    });

    $("#nav_menu a").click(function(event){
        event.preventDefault()
        let menu = $.trim($(this).find(".name").text())
        let room_name = $(this).data('room')
        $(this).find(".notif").addClass("sr-only");
        $(this).find(".notif").text(0);
        idle = room_name
        $("#panel_name").text(menu)
        $(this).tab('show')
        loadMessage(room_name)
    })

    connect();
    
    $("#schedule_meet").submit(function(event){
        event.preventDefault()
        window.open('/setup')
        document.getElementById("schedule_meet").reset();
        $("#MeetingModal").modal('hide')
    })

    $("#close").click(function(){
        window.close()
    })

    $("#join_meet").submit(function(){
        event.preventDefault()
        const room_id = $("#room_id").val()
        window.open('/room/'+room_id)
        document.getElementById("join_meet").reset()
        $("#JoinMeetModal").modal('hide')
    })

    $("#sidebarToggle").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });

    $("#list-contact a").on('click', function(e){
        e.preventDefault()
    })

    $(".init-chat").click(async function(){
        // let recent_chat = $(".r-chat")
        
        // for(let i=0; i < recent_chat.length; i++){
        //     console.log(recent_chat[i])
        // }
        let user = {
            dest : $(this).data('user')
        }

        let response = await fetch('/home/check/', {
            method : 'POST',
            headers : {
                'Content-type' : 'application/json',
                'X-CSRFToken' : $('input[name=csrfmiddlewaretoken]').val()
            },
            body : JSON.stringify(user)
        })

        console.log(await response.json());
    })
})