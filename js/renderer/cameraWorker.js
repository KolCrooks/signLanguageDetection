let camera = 0;

let setCamera = (selected) => {
	camera = selected;
};

let renderImage = () => {

	navigator.mediaDevices.getUserMedia({
		audio:false,
		video: {
			deviceId: {exact: camera}
	  	}
	})
	.then(function(stream) {
		let video = $("#video")[0];
		console.log(stream)
		video.srcObject = stream;
		video.onloadedmetadata = function(e) {
			console.log(e)
		  video.play();
		};
	}).catch(e=>{console.error(e)})
}

module.exports = {
	setCamera,
	renderImage
};