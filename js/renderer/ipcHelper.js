const {ipcRenderer} = require("electron");



let setCamera = async (selected) => {

	ipcRenderer.send("setCamera",selected);

	ipcRenderer.once("setCamera", (event, arg) => {
		let response = JSON.parse(arg);
		if(!response.res)
			console.log(response);
		return response.res;
	});
};

ipcRenderer.on("curFrame", async (event, arg) => {

	let response = JSON.parse(arg);
	if(!response.res) return;
	data = JSON.parse(response.data);
	dim = response.dim;
	canvas = document.getElementById("output");
	let {data, dim} = await ipcHelper.getFrame();
	renderImage(data.data, dim,canvas);

});

function renderImage(data, dim, canvas) {

	canvas.height = dim[0];
	canvas.width = dim[1];

	var ctx = canvas.getContext("2d");
	var dataImage = ctx.createImageData(dim[0], dim[1]);
	dataImage.data.set(new Uint8ClampedArray(data));
	ctx.putImageData(dataImage,0,0);
}

module.exports = {
	setCamera,
	ipcRenderer
};