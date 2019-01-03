const {ipcRenderer} = require("electron");
// let pc = new RTCPeerConnection();

// let addTrack = (stream) => {
// 	pc.addTrack(stream.getTracks()[0], stream);
// };
ipcRenderer.on("offer", function(event){
	console.log(event)
})

module.exports = {
	//addTrack,
	//pc
};