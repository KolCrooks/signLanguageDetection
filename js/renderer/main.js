let electron = require("electron").remote;
let cameraWorker = require("../js/renderer/cameraWorker");
let networkHelper = require("../js/renderer/networkRenderer");
let recorder = require('../js/renderer/recorder');
let videoCapture = require("../js/renderer/VideoCapture");
var Client = require("../js/renderer/client");
var imageProc = require('../js/renderer/imgProc');

$ = window.$;


let init = async function(){
	await updateDevices();

	let cameraSelect = $("#cameraSelect");
	cameraSelect.click(updateDevices);
	cameraSelect.change(()=>{
		console.log("cameraChange",cameraSelect.val());
		cameraWorker.setCamera(cameraSelect.val());
	});

	console.log("cameraChange",cameraSelect.val());
	cameraWorker.setCamera(cameraSelect.val());
	cameraWorker.attachCamera().then((video)=>{

		video.width = video.videoWidth;
		video.height = video.videoHeight;
		let dummyCanvas = document.getElementById('dummy');

		videoCapture = new videoCapture(video, dummyCanvas);
		recorder = new recorder(video);

		$('#record').click(recorder.toggle);
		$("#loadingDIV").fadeOut(750);

	}).catch(e=>{console.error(e)})
	

};


let updateDevices = async ()=> {
	console.log("updating devices");
	let devices = await cameraWorker.detectCameras();
	devices.forEach(element => {
		$("#cameraSelect").find("option")
			.remove()
			.end();
		$("#cameraSelect").append("<option value="+ element.deviceId + ">" + element.label + "</option>");
	});
};

$(document).ready(()=> {
	init().then(()=>{console.log("Done Loading.")});
});

