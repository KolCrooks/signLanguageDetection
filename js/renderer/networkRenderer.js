const {ipcRenderer} = require("electron");
let udp = require('datagram-stream');

let stream = null

let createStream = (ip) =>{
    stream = udp({
        address: '0.0.0.0',   //address to bind to
        unicast: ip, //unicast ip address to send to
        port      : 31419,        //udp port to send to
        bindingPort : 31420,      //udp port to listen on. Default: port
        reuseAddr : false,        //boolean: allow multiple processes to bind to the
                                  //         same address and port. Default: true
    });
}


ipcRenderer.on("offer", function(event){
	console.log(event)
})

let saveBlob = (blob,fileName) => {
    let reader = new FileReader()
    reader.onload = function() {
        if (reader.readyState == 2) {
            var buffer = new Buffer(reader.result)
            ipcRenderer.send("SAVE_FILE", fileName, buffer)
            console.log(`Saving ${JSON.stringify({ fileName, size: blob.size })}`)
        }
    }
    reader.readAsArrayBuffer(blob)
}

let send_frame = (frame) =>{

}

module.exports = {
	saveBlob
};