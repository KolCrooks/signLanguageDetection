let cv = require('opencv4nodejs');
let imageProc = require('../js/imgProc');
let VideoCapture = function(videoElement, canvasDummy){
    videoElement.addEventListener('timeupdate', capture, false);

    canvasDummy.width = videoElement.videoWidth;
    canvasDummy.height = videoElement.videoHeight;
    let ctx = canvasDummy.getContext('2d');

    function capture() {
        ctx.drawImage(this, 0, 0, canvasDummy.width, canvasDummy.height);

        // load base64 encoded image
        let base64data = canvasDummy.toDataURL().replace('data:image/jpeg;base64','')
            .replace('data:image/png;base64','');//Strip image type prefix
        let buffer = Buffer.from(base64data,'base64');
        let image = cv.imdecode(buffer); //Image is now represented as Mat
        imageProc.procAndPool(image);
    }

    this.send = function(){
        imageProc.sendPool();
    }

};

module.exports = VideoCapture;