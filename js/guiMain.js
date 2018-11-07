/*
 * This is a project for an AP chem research project
 * Software is under Apache License 2.0
 * @Author: kol.crooks && sean.mcHale
 * @Date: 2018-10-01
 */
var electron = require('electron');
var ipcMain = require('./ipcMain');

if(process.execPath.indexOf('electron') > -1) {
    // it handles shutting itself down automatically
    require('electron-local-crash-reporter').start();
  }

let init = function(os){
    electron.app.on('ready',createWindow);
}


function createWindow () {
    // Create the browser window.
    win = new electron.BrowserWindow({
        webPreferences: {
            nodeIntegrationInWorker: true
        },
        width: 800,
        height: 600
        });
  
    // and load the index.html of the app.
    win.loadFile('./web/index.html');
}


module.exports = {
    init
}