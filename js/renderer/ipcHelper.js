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
let getFrame = async () => {
	return new Promise((resolve, reject) => {
		ipcRenderer.send("getFrame");

		ipcRenderer.once("getFrame", (event, arg) => {

			let response = JSON.parse(arg);
			if(!response.res)
				reject(response.error);
			resolve({data: JSON.parse(response.data), dim: response.dim});

            
		});
	});

};

module.exports = {
	setCamera,
	getFrame,
	ipcRenderer
};