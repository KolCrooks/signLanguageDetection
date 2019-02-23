let electron = require("electron").remote;
let cameraWorker = require("../js/renderer/cameraWorker");
let networkHelper = require("../js/renderer/networkRenderer")
let cv = require('../lib/opencv')
let recorder = require('../js/renderer/recorder')
$ = window.$;



electron.getCurrentWindow().toggleDevTools();

var src;
var dst;
var dst2;
var cap;
var canvasFrame;
var canvas2;


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
				// canvasFrame = document.getElementById("output");


				// video.width = video.videoWidth;
				// video.height = video.videoHeight;

				// canvasFrame.width = video.videoWidth;
				// canvasFrame.height = video.videoHeight;
				// $(canvasFrame).css("width","25vw");
				// $(canvasFrame).css("height","auto");
				
				// src = new cv.Mat(video.videoHeight, video.videoWidth, cv.CV_8UC4);
				// dst = new cv.Mat(video.videoHeight, video.videoWidth, cv.CV_8UC1);
				// cap = new cv.VideoCapture(video);
				recorder.init(video);
				$('#record').click(recorder.toggle)
				$("#loadingDIV").fadeOut(1000);
				// dst2 = dst.clone();
				setTimeout(processVideo, 0);
			})();
	},10000);


	}).catch(e=>{console.error(e)})
	

};


var updateDevices = async ()=> {
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
function processVideo() {
	let begin = Date.now();
	// cap.read(src);
	// cv.imshow("output", src);
	// src.convertTo(dst, -1, parseFloat(document.getElementById("min").value) || 0.1, parseFloat(document.getElementById("max").value) || 1);
	// // cv.cvtColor(dst, dst2, cv.COLOR_RGBA2GRAY);
	// cv.Canny(dst, dst2, 30, 60, 3, false);
	// let contours = new cv.MatVector();
	// let hierarchy = new cv.Mat();
	// let temp = dst2.clone()
	// console.log("1")
	
	// cv.findContours(dst2, contours, hierarchy, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE);
	// cv.filterContours()
	// draw contours
	// cv.drawContours(temp, contours, -1, new cv.Scalar(255,255,255), 1, cv.LINE_8, hierarchy, 100);
	// console.log("3")

	// contours.delete();
	// hierarchy.delete();
	// cv.imshow("output", dst);
	// cv.imshow("output2", dst2);
	// temp.delete();

    // schedule next one.
    let delay = 1000/FPS - (Date.now() - begin);
    setTimeout(processVideo, delay);
}
// schedule first one.

$(document).ready(()=> {
	init();
});

global.networkHelper = networkHelper;