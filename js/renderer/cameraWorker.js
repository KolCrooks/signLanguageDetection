let camera = 0;
let video;
let setCamera = (selected) => {
	camera = selected;
};

let renderImage = ()=> {return new Promise((resolve, reject) => {

	navigator.mediaDevices.getUserMedia({
		audio:false,
		video: {
			deviceId: {exact: camera}
	  	}
	})
	.then(function(stream) {
		video = $("#video")[0];
		console.log(stream);
		video.srcObject = stream;
		video.onloadedmetadata = function(e) {
			console.log(e)
		  video.play().then(()=>{resolve(video);});
		  
		};
		
	}).catch(e=>{reject(e)})
})};
let getCamera = () => { 
	return video;
}
var detectCameras = async function (){
	let devices = await navigator.mediaDevices.enumerateDevices();
	let cams = [];
	devices.forEach((v)=>{
		if(v.kind == "videoinput") cams.push(v);
	});
	return cams;
};
module.exports = {
	setCamera,
	renderImage,
	getCamera,
	detectCameras
};