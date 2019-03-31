let ipc = require('./networkRenderer');
const { app } = require('electron').remote


/**
 * This adds support for the recording of a canvas element
 * @param {HTMLCanvasElement} canvas: the canvas element that you want to record
 */
let recorder = function(canvas){
    let stream;
    let recorder;
    let recordChunks = [];
    let recording = false;

    const options = {
        message: "File Path?",
        defaultPath: app.getPath('documents') + "/clip.webm",
    };

    stream = canvas.captureStream();

    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = function(e) {
        recordChunks.push(e.data);
    };

    recorder.onerror = function(e){
        console.error(e);
    };

    /**
     * start recording the canvas
     */
    let start = function(){
        recordChunks = [];
        recorder.start(100);
        console.log("recoding startesd")
        $('#record').html("stop")
        recording = true;
    };

    this.toggle = function(){
        if(!recording)
            start();
        else
            stop();
    };

    /**
     * Stop Recording the canvas and save the video
     */
    stop = function(){
        recorder.stop();
        console.log("recoding Stopped")
        //dialog.showSaveDialog(null, options,save);
        save("./clips/" + new Date().getTime() + ".webm");
        $('#record').html("record")
        recording = false;
    };
    /**
     * Pause Capture
     */
    this.pause = function(){
        recorder.pause();
    };

    /**
     * Save the current buffer pool to a file location
     * @param location
     */
    let save = function(location){
        // dialog.showMessageBox(null, {title: "Saved File"})
        const fullBlob = new Blob(recordChunks);
        ipc.saveBlob(fullBlob,location);
    }
};


module.exports = recorder;