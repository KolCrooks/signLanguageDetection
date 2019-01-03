/*
 * This is a project for an AP chem research project
 * Software is under Apache License 2.0
 * @Author: Kol.Crooks && sean.McHale
 * @Date: 2018-10-01
 */
var electron = require('electron');
var ipcMain = require('./networkMain');



let init = function(os){
    electron.app.on('ready',createWindow);
}


function createWindow () {
    // Create the browser window.
    win = new electron.BrowserWindow({
        webPreferences: {
            nodeIntegrationInWorker: true
        },
        width: 1200,
        height: 600
        });
  
    // and load the index.html of the app.
    win.loadFile('./web/index.html');
}


module.exports = {
    init
}