let net = require('net');

/**
 * This is a TCP client for communicating with the classification server
 * @param ip The IP of the server
 * @param port port of the server
 */
let client = function(ip = "localhost", port = 9999){
    let options = {
        host: ip,
        port: port
    };

    // Create TCP client.
    let client = net.createConnection(options, function () {
        console.log('Connection local address : ' + client.localAddress + ":" + client.localPort);
        console.log('Connection remote address : ' + client.remoteAddress + ":" + client.remotePort);
    });

    client.setTimeout(1000);
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
        console.error(JSON.stringify(err));
    });

    /**
     * Sends the frames of objects to the server for classification
     * @param frames: int[][][] of frames
     */
    this.sendFrames = function(frames){

        let obj = {
            frames: frames,
            size: [frames[0].length, frames[0][0].length],
        };

        let bytes = JSON.stringify(obj).toUTF8Array();
        //MAX CHUNK SIZE IS 1400 BYTES (1 less byte to keep room for the state byte)
        let chunks = chunkArray(bytes, 1399);
        for (let i = 0; i < chunks.length - 1; i++) {
            client.write(new Buffer([0x0].concat(chunks[i])));
        }
        client.write(new Buffer([0x01].concat(chunks[chunks.length - 1])))
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

    String.prototype.toUTF8Array = ()=>{
        let str = this;
        let utf8 = [];
        for (let i=0; i < str.length; i++) {
            let charcode = str.charCodeAt(i);
            if (charcode < 0x80) utf8.push(charcode);
            else if (charcode < 0x800) {
                utf8.push(0xc0 | (charcode >> 6),
                    0x80 | (charcode & 0x3f));
            }
            else if (charcode < 0xd800 || charcode >= 0xe000) {
                utf8.push(0xe0 | (charcode >> 12),
                    0x80 | ((charcode>>6) & 0x3f),
                    0x80 | (charcode & 0x3f));
            }
            // surrogate pair
            else {
                i++;
                // UTF-16 encodes 0x10000-0x10FFFF by
                // subtracting 0x10000 and splitting the
                // 20 bits of 0x0-0xFFFFF into two halves
                charcode = 0x10000 + (((charcode & 0x3ff)<<10)
                    | (str.charCodeAt(i) & 0x3ff));
                utf8.push(0xf0 | (charcode >>18),
                    0x80 | ((charcode>>12) & 0x3f),
                    0x80 | ((charcode>>6) & 0x3f),
                    0x80 | (charcode & 0x3f));
            }
        }
        return utf8;
    };

    Array.prototype.insert = function ( index, item ) {
        this.splice( index, 0, item );
    };
};

module.exports.client = client;
