let camera = 0;
let video;
let setCamera = (selected) => {
	camera = selected;
};

/**
 * This sets up the
 * @returns {Promise<HTMLVideoElement>} returns the video element that has been set up
 */
let attachCamera = ()=> {return new Promise((resolve, reject) => {

	//Get the camera device
	navigator.mediaDevices.getUserMedia({
		audio:false,
		video: {
			deviceId: {exact: camera}
	  	}
	})
		//Attach the camera device to the video element
	.then(function(stream) {
		video = $("#video")[0];
		video.srcObject = stream;
		video.onloadedmetadata = function(e) {
			console.log(stream.getVideoTracks()[0].getSettings())
		  video.play().then(()=>{resolve(video);});

		};
		
	}).catch(e=>{reject(e)})
})};

/**
 * Get the camera element
 * @returns {HTMLVideoElement}
 */
let getCamera = () => { 
	return video;
};

/**
 * Looks for a camera
 * @returns {Promise<Array>}
 */
let detectCameras = async function (){
	let devices = await navigator.mediaDevices.enumerateDevices();
	let cams = [];
	devices.forEach((v)=>{
		if(v.kind === "videoinput") cams.push(v);
	});
	return cams;
};
module.exports = {
	setCamera,
	attachCamera,
	getCamera,
	detectCameras
};