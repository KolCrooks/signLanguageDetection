let cv = require('opencv4nodejs');
let client = require("../js/renderer/client");
client = new client();

let pool = [];

let procAndPool = function(Mat){
    let frame = proc(Mat);
    pool.append(cv.imencode('.jpg', frame).toString('base64'));
};

let proc = function(Mat){
    let gray = Mat.cvtColor(cv.COLOR_RGB2GRAY);
    return gray.resize(60, 60);
};

let sendPool = function(){
    client.sendFrames(pool);
    pool = []
};

module.exports = {
    procAndPool,
    proc,
    sendPool
};