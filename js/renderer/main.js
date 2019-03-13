let electron = require("electron").remote;
let cameraWorker = require("../js/renderer/cameraWorker");
let networkHelper = require("../js/renderer/networkRenderer")
let cv = require('../lib/opencv')
let utils = new Utils('')
let recorder = require('../js/renderer/recorder')
let handTraack = require('handtrackjs')
$ = window.$;


// if(electron.getCurrentWindow().is)
	// electron.getCurrentWindow().toggleDevTools();

let src;
let dst;
let dst2;
let cap;
let canvasFrame;
let canvas2;
let handClassifiers = [];
let classifierFiles = ["aGest.xml", "fist.xml", "closed_frontal_palm.xml"];
let detections = [];

let init = async function(){
	await updateDevices();

	$("#cameraSelect").click(updateDevices);
	$("#cameraSelect").change(()=>{
		console.log("cameraChange",$("#cameraSelect").val());
		cameraWorker.setCamera($("#cameraSelect").val());
	});

	console.log("cameraChange",$("#cameraSelect").val());
	cameraWorker.setCamera($("#cameraSelect").val());
	cameraWorker.renderImage().then((video)=>{
		setTimeout(()=>{
			(()=>{
				canvasFrame = document.getElementById("output");


				video.width = video.videoWidth;
				video.height = video.videoHeight;

				canvasFrame.width = video.videoWidth;
				canvasFrame.height = video.videoHeight;
				$(canvasFrame).css("width","25vw");
				$(canvasFrame).css("height","auto");
				
				src = new cv.Mat(video.videoHeight, video.videoWidth, cv.CV_8UC4);
				dst = new cv.Mat(video.videoHeight, video.videoWidth, cv.CV_8UC1);
				cap = new cv.VideoCapture(video);
				recorder.init(video);
				$('#record').click(recorder.toggle);
				handTrack.load().then(model => {
					// detect objects in the image.
					console.log("handtrack loaded")
					$("#loadingDIV").fadeOut(1000);
					setTimeout(()=>processVideo(model,video), 0);
				});

			})();
	},10000);


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

const FPS = 30;

function processVideo(model,video) {
	let beginning = Date.now();
	model.detect(video).then(predictions => {
		console.log('Predictions: ', predictions);

		let delay = 1000/FPS - (Date.now() - beginning);
		setTimeout(()=>processVideo(model,video), delay);
	});
}
// schedule first one.

$(document).ready(()=> {
	init();
});

