const cluster = require('cluster');
const camera = require('./camera');
const {ipcMain} = require('electron');

var running = true;
var pause = false;



const FPS = 15;
function loop() {
    try {
        if(!running) return;

        let frame = camera.getCurrentFrame();
        sendFrame(frame);

        // schedule the next one.
        let delay = 1000/FPS - (Date.now() - begin);
        setTimeout(processVideo, delay);
    } catch (err) {
        utils.printError(err);
    }
};


let main = ()=>{
    setTimeout(loop, 0);
}



cluster.worker.on('message',(msg)=>{
    switch(msg.cmd){
        case "shutdown":
            running = false;
            pause = true;
        break; 
        case "pause":
            pause = !pause;
        break;
    }
});

let sendFrame = (data)=> {
    event.sender.send('curFrame', JSON.stringify(data));
};

ipcMain.on('setCamera', (event, arg) => {
    
    let answer = camera.setCamera(arg);
    event.sender.send('setCamera', JSON.stringify(answer));
});

module.exports = {
    running,
    main
}