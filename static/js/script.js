$(function(){

   setInterval(update, 500);

    $("#send").click(function(){
        let chat = $("#chat").val()
        let csrftoken  = $('input[name=csrfmiddlewaretoken]').val()

        $.ajax({
            url: '/home/req/',
            type: "post",
            dataType: 'json',
            data : {
                chat : chat,
                csrfmiddlewaretoken : csrftoken
            },
            success: function(data){
                console.log(data)
                //$("#chat-field").append("<span class='badge badge-pill badge-secondary py-2 px-2 my-1' style='font-size: 15px'>"+data+"</span><br>")
                $("#chat").val('')
            }
        })
    })

    function update(){
        $.ajax({
            url : '/home/get_message/',
            type: 'get',
            dataType : 'json',
            success: function(data) {
                if(data != 'empty' && data != 'blom'){
                    $("#chat-field").append("<span class='badge badge-pill badge-secondary py-2 px-2 my-1' style='font-size: 15px'>"+data+"</span><br>")
                }
            }
        });
    }
})

