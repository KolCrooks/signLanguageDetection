const {ipcRenderer} = require("electron");
// let pc = new RTCPeerConnection();

// let addTrack = (stream) => {
// 	pc.addTrack(stream.getTracks()[0], stream);
// };
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

module.exports = {
	saveBlob
};