const socket = new WebSocket("ws://127.0.0.1:5576");

const peers = new Peer();
let videoGrid = document.getElementById('video-grid')

let myVideo = document.createElement('video')
myVideo.muted = true

let stream = ''
let micBtn = document.getElementById('mic-btn')
let videoBtn = document.getElementById('video-btn')
let disconnectBtn = document.getElementById('end-call')
const users = {}

async function setVideo(){
    stream = await navigator.mediaDevices.getUserMedia({
        video : true,
        audio : true
    })
    
    stream.getAudioTracks()[0].enabled = false

    const videoWrapper = document.createElement('div')
    addVideoStream(myVideo, videoWrapper, stream)
}

micBtn.addEventListener('click', () => {
    if(stream.getAudioTracks()[0].enabled){
        stream.getAudioTracks()[0].enabled = false
        document.getElementById('mic-logo').classList.remove('fa-microphone')
        document.getElementById('mic-logo').classList.add('fa-microphone-slash')
    }
    else{
        stream.getAudioTracks()[0].enabled = true
        document.getElementById('mic-logo').classList.remove('fa-microphone-slash')
        document.getElementById('mic-logo').classList.add('fa-microphone')
    }
})

videoBtn.addEventListener('click', () => {
    if(stream.getVideoTracks()[0].enabled){
        stream.getVideoTracks()[0].enabled = false
        document.getElementById('video-logo').classList.remove('fa-video')
        document.getElementById('video-logo').classList.add('fa-video-slash')
    }
    else{
        stream.getVideoTracks()[0].enabled = true
        document.getElementById('video-logo').classList.remove('fa-video-slash')
        document.getElementById('video-logo').classList.add('fa-video')
    }
})


setVideo()

socket.addEventListener('message', (event) => {
    console.log("there's a new message")
    let new_msg = JSON.parse(event.data)

    if(new_msg.action == 'user-connected'){
        connectedNewUser(new_msg.user_id, stream)    
    }
    else if(new_msg.action == 'user-disconnected'){
        if(users[new_msg.user_id]){
            users[new_msg.user_id].close()
        }
    }
})

peers.on('open', id => {
    let message = {
        action : 'join-room',
        room_id : ROOM_ID,
        user_id : id
    }
    message = JSON.stringify(message)
    socket.send(message)
})

peers.on('call', call => {
    call.answer(stream)

    const video = document.createElement('video')
    const videoWrapper = document.createElement('div')
    
    call.on('stream', userVideoStream => {
        addVideoStream(video, videoWrapper, userVideoStream)
    })

    call.on('close', () => {
        video.parentElement.remove()
    })

    users[call.peer] = call
})

function addVideoStream(video, videoWrapper, stream){
    videoWrapper.classList.add('col-3','p-1')

    video.srcObject = stream;
    video.addEventListener('loadedmetadata', function(){
        video.play();
    });
    videoWrapper.append(video)
    videoGrid.append(videoWrapper)
}

function connectedNewUser(userId, stream){
    const call = peers.call(userId, stream)
    const video = document.createElement('video')
    const videoWrapper = document.createElement('div')
    call.on('stream', (userVideoStream) => {
        addVideoStream(video, videoWrapper, userVideoStream)
    })

    call.on('close', () => {
        video.parentElement.remove()
    })

    users[userId] = call
}
// const socket = io('http://127.0.0.1:5576')
// const peer = new Peer()
// const videoGrid = $("#video-grid")
// let stream = ''
// let myVideo = document.createElement('video')

// const users = {}

// peer.on('open', id => {
//     console.log("my user id :",id)
//     socket.emit('join-room', ROOM_ID, id)
// })

// peer.on('call', call => {
//     call.answer(stream)

//     const video = document.createElement('video')
//     call.on('stream', (userVideoStream) => {
//         addVideoStream(video, userVideoStream)
//     })
// })

// socket.on('user-connected', user_id => {
//     connectedNewUser(user_id, stream)
// })

// socket.on('user-disconnected', user_id => {
//     if(users[user_id]){
//         users[user_id].close()
//     }
//     else{
//         close()
//     }
// })

// async function setVideo(){
//     stream = await navigator.mediaDevices.getUserMedia({
//         video : true,
//         audio : true
//     })

//     addVideoStream(myVideo, stream)

//     close()
// }

// function addVideoStream(video, stream){
//     video.srcObject = stream;
//     video.addEventListener('loadedmetadata', function(){
//         video.play();
//     });
//     videoGrid.append(video)
// }

// function connectedNewUser(userId, stream){
//     const call = peer.call(userId, stream)
//     const video = document.createElement('video')
//     call.on('stream', (userVideoStream) => {
//         addVideoStream(video, userVideoStream)
//     })

//     call.on('close', () => {
//         video.remove()
//     })

//     users[userId] = call
// }

// setVideo()