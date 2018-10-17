
const {ipcMain} = require('electron');
const camera = require('./camera');



ipcMain.on('setCamera', (event, arg) => {
  let answer = camera.setCamera(arg);

  event.sender.send('setCamera', JSON.stringify(answer));

});

ipcMain.on('getFrame', (event, arg) => {
  event.sender.send('getFrame', JSON.stringify(camera.getCurrentFrame()));
  
});
