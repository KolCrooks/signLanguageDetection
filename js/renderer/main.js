let electron = require("electron").remote;
let ipcHelper = require("../js/renderer/ipcHelper");
let cv = require("opencv4nodejs");
$ = window.$;



electron.getCurrentWindow().toggleDevTools();

let init = async function(){
	await updateDevices();
	$("#cameraSelect").click(updateDevices);
	$("#cameraSelect").change(()=>{
		console.log("cameraChange",$("#cameraSelect").val());
		ipcHelper.setCamera(parseInt($("#cameraSelect").val()));
	});

	console.log("cameraChange",$("#cameraSelect").val());
	ipcHelper.setCamera(parseInt($("#cameraSelect").val()));

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
		$("#cameraSelect").append("<option value="+ devices.indexOf(element) + ">" + element.label + "</option>");
	});
};


$(document).ready(()=> {
	init();


});

global.ipcHelper = ipcHelper;