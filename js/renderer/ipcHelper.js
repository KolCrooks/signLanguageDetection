const {ipcRenderer} = require('electron')

let setCamera = async (selected) => {

    ipcRenderer.send('setCamera',selected);
    ipcRenderer.once('setCamera', (event, arg) => {
        let response = JSON.parse(arg);
        if(!response.res)
        console.log(response)
        return response.res;
     })
}


module.exports = {
    setCamera,
    ipcRenderer
}