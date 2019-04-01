let net = require('net');

/**
 * This is a TCP client for communicating with the classification server
 * @param ip The IP of the server
 * @param port port of the server
 */
let client = function(ip = "localhost", port = 31419){
    let options = {
        host: ip,
        port: port
    };

    // Create TCP client.
    let client = net.createConnection(options, function () {
        console.log('Connection local address : ' + client.localAddress + ":" + client.localPort);
        console.log('Connection remote address : ' + client.remoteAddress + ":" + client.remotePort);
    });

    client.setTimeout(0);
    client.setEncoding('utf8');

    // When receive server send back data.
    client.on('data', function (data) {
        console.log('Server return data : ' + data);
    });

    // When connection disconnected.
    client.on('end',function () {
        console.log('Client socket disconnect. ');
    });

    client.on('timeout', function () {
        console.log('Client connection timeout. ');
    });

    client.on('error', function (err) {
        console.error(err);
    });

    /**
     * Sends the frames of objects to the server for classification
     * @param frames: int[][][] of frames
     */
    this.sendFrames = function(frames){
        console.log(`Sending ${frames.length} frames`);
        let obj = {
            frames: frames,
            size: [frames[0].length, frames[0][0].length],
        };

        let s = JSON.stringify(obj);
        let utf8 = unescape(encodeURIComponent(s));
        let arr = [];
        for (let i = 0; i < utf8.length; i++) {
            arr.push(utf8.charCodeAt(i));
        }
        console.log(s.length);

        //MAX CHUNK SIZE IS 1400 BYTES (1 less byte to keep room for the state byte)
        let chunks = chunkArray(arr, 1399);
        console.log(`Sending ${chunks.length} chunks`)
        for (let i = 0; i < chunks.length - 1; i++) {
            let tempBuf = new Buffer([0x0].concat(chunks[i]));
            client.write(tempBuf);
        }
        let tempBuf = new Buffer([0x01].concat(chunks[chunks.length - 1]));
        console.log('Writing Buffer', tempBuf);

        client.write(tempBuf)
    };

    /**
     * Returns an array with arrays of the given size.
     *
     * @param myArray {Array} Array to split
     * @param chunkSize {Integer} Size of every group
     */
    function chunkArray(myArray, chunk_size){
        let results = [];

        while (myArray.length) {
            results.push(myArray.splice(0, chunk_size));
        }

        return results;
    }

    Array.prototype.insert = function ( index, item ) {
        this.splice( index, 0, item );
    };
};

module.exports.client = client;
