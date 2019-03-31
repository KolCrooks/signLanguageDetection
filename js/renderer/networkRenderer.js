const {ipcRenderer} = require("electron");

ipcRenderer.on("offer", function(event){
	console.log(event)
});

let saveBlob = (blob,fileName) => {
    let reader = new FileReader();
    reader.onload = function() {
        if (reader.readyState === 2) {
            let buffer = new Buffer(reader.result);
            ipcRenderer.send("SAVE_FILE", fileName, buffer);
            console.log(`Saving ${JSON.stringify({ fileName, size: blob.size })}`)
        }
    };
    reader.readAsArrayBuffer(blob)
};

module.exports = {
	saveBlob
};