let ipc = require('./networkRenderer');
const { dialog, app } = require('electron').remote

const options = {
  message: "File Path?",
  defaultPath: app.getPath('documents') + "/clip.webm",
}


let stream;
let recorder;
let recordChunks = [];
let recording = false;
let init = (canvas)=>{

    stream = canvas.captureStream();

    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = function(e) {
        recordChunks.push(e.data);
        console.log(recordChunks.length)
    }
    recorder.onerror = function(e){
        console.error(e);
    }
    
}
let toggle = ()=>{
    if(recording)
        stop();
    else
        start();
}
let start = ()=>{
    recordChunks = [];
    recorder.start(100);
    console.log("recoding startesd")
    $('#record').html("stop")
    recording = true;
}
let stop = ()=>{
    recorder.stop();
    console.log("recoding Stopped")
    //dialog.showSaveDialog(null, options,save);
    save("./clips/" + new Date().getTime() + ".webm");
    $('#record').html("record")
    recording = false;
}
let pause = ()=>{
    recorder.pause();
}
let getChunks = () =>{
    return recordChunks.length;
}

let save = (location)=>{
    // dialog.showMessageBox(null, {title: "Saved File"})
    const fullBlob = new Blob(recordChunks);
    ipc.saveBlob(fullBlob,location);
}
module.exports = {
    start,
    stop,
    pause,
    getChunks,
    save,
    init,
    toggle,
    stream,
    recorder,
}
