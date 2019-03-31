const {ipcMain} = require('electron');
let fse = require('fs-extra');

ipcMain.on("SAVE_FILE", (event, path, buffer) => {
  fse.outputFile(path, buffer, err => {
      if (err) {
          event.sender.send("ERROR", err.message)
      } else {
          event.sender.send("SAVED_FILE", path)
      }
  })
});