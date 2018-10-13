const cv = require('opencv4nodejs');

/**
 * @summary Set the capture device for the camera object
 * @param {Int} device The device id 
 */
var setCamera = (device) => {
    try{
        capDevice = cv.VideoCapture(device);
        return {
            res: true,
            device: device,
            error: ""
        }
    }catch(e){
        return {
            res: false,
            device: device,
            error: e.message
        } 
    }
}


/**
 * @summary Get the current frame from the capture device
 * @returns returns a Mat object of frame
 */
var getCurrentFrame = () => {
    return capDevice.read();
}


module.exports = {
    setCamera,
    getCurrentFrame
}
