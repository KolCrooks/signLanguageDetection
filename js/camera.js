const cv = require('opencv4nodejs');
var capDevice;

global.cv = cv;

/**
 * @summary Get camera list
 * @returns {Object[]} camera list
 */
var detectCameras = async function (){
    let devices = await navigator.mediaDevices.enumerateDevices();
    let cams = [];
    devices.forEach((v)=>{
        if(v.kind == "videoinput") cams.push(v);
    });
    return cams
}

/**
 * @summary Set the capture device for the camera object
 * @param {Int} device The device id 
 */
var setCamera = function(device){
    capDevice = cv.VideoCapture(device);
}

/**
 * 
 * @returns returns a Mat object of frame
 */
var getCurrentFrame = function(){
    return capDevice.read();
}


module.exports = {
    detectCameras,
    setCamera,
    getCurrentFrame
}
