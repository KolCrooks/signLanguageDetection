let electron = require("electron").remote;
let cameraWorker = require("../js/renderer/cameraWorker");
let networkHelper = require("../js/renderer/networkRenderer")
const cv = require('../lib/opencv')
$ = window.$;



electron.getCurrentWindow().toggleDevTools();

var src;
var dst;
var dst2;
var cap;
var canvasFrame;

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
				src = new cv.Mat(video.videoHeight, video.videoWidth, cv.CV_8UC4);
				dst = new cv.Mat(video.videoHeight, video.videoWidth, cv.CV_8UC1);
				cap = new cv.VideoCapture(video);
				dst2 = cv.Mat.zeros(video.videoHeight, video.videoWidth, cv.CV_8UC1);
				setTimeout(processVideo, 0);
			})();
	},10000);


	}).catch(e=>{console.error(e)})
	

};

var detectCameras = async function (){
	let devices = await navigator.mediaDevices.enumerateDevices();
	let cams = [];
	devices.forEach((v)=>{
		if(v.kind == "videoinput") cams.push(v);
	});
	return cams;
};

var updateDevices = async ()=> {
	console.log("updating devices");
	let devices = await detectCameras();
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
    cap.read(src);
	cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
	cv.Canny(dst, dst, 50, 100, 3, false);
	let contours = new cv.MatVector();
	let hierarchy = new cv.Mat();
	let temp = dst2.clone()
	console.log("1")
	// You can try more different parameters
	cv.findContours(dst, contours, hierarchy, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE);
	// draw contours with random Scalar
	console.log("2")
	cv.drawContours(temp, contours, -1, new cv.Scalar(255,255,255), 1, cv.LINE_8, hierarchy, 100);
	console.log("3")

	contours.delete();
	hierarchy.delete();
	cv.imshow("output", temp);
	temp.delete();
	dst2.clear
    // schedule next one.
    let delay = 1000/FPS - (Date.now() - begin);
    setTimeout(processVideo, delay);
}
// schedule first one.

$(document).ready(()=> {
	init();
	
});

global.networkHelper = networkHelper;