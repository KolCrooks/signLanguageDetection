let camera = require('../js/camera');
let electron = require('electron').remote;
$ = window.$;

electron.getCurrentWindow().toggleDevTools();

devices = []
let init = function(){
    camera.detectCameras().then((r)=>{
        let cnt = 0;
        devices = r
        r.forEach(element => {
            $('#cameraSelect').append("<option value="+ element.deviceId + ">" + element.label + "</option>");
        });
        navigator.mediaDevices.getUserMedia({
            video: {
                deviceId: $('#cameraSelect').val()
            },
            audio: false,
        }).then(stream =>{
            let video = document.getElementById("camera");
            video.srcObject = stream;
            video.play();
            console.log(video)
            camera.setCamera(video);
            console.log(camera.getCurrentFrame())
        });

    });

}

init()