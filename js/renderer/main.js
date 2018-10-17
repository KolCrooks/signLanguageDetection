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
	cameraLoop();

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
var cameraLoop = () =>{
	setInterval(async ()=>{
		let {data, dim} = await ipcHelper.getFrame();
		let canvas = document.getElementById("output");
		renderImage(data, dim,canvas);
		
	},1000);
};

function renderImage(data, dim, canvas) {

	canvas.height = dim[0];
	canvas.width = dim[1];

	var ctx = canvas.getContext("2d");
	var palette = ctx.getImageData(0,0,dim[0],dim[1]);
	palette.data.set(new Uint8ClampedArray(data));
	
	ctx.putImageData(palette,0,0);
}

$(document).ready(()=> {
	init();


});

global.ipcHelper = ipcHelper;