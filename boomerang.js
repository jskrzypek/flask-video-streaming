var rp = require('request-promise');
var util = require('util');
var btoa = require('btoa');
setInterval(function() {
    sending();
    // setTimeout(function() {
    //     sending();
    // }, 1000);
}, 1000);


// var sending = function() {
//    return rp('http://10.0.0.2:8080/live.jpg')
//        .then(function(body) {
//            return btoa(body);
//        })
//        .then(function(content) {
//            var options = {
//                method: 'POST',
//                uri: 'http://localhost:5000/upload_frame',
//                body: {
//                    content: content
//                },
//                json: true // Automatically stringifies the body to JSON 
//            };

//            return rp(options);
//        })
//        .catch(function(err) {
//            console.log('ERR', err);
//        });
// };


var sending = function() {
    // return rp('http://10.0.0.1:8080/live.jpg')
    // return rp('http://10.26.107.39:8080/live.jpg')
    return rp({
            // uri: 'http://10.10.14.148:8080/live.jpg',
            uri: 'http://localhost:5000/cv_feed',
            resolveWithFullResponse: true,
            encoding: null
        })
        .then(function(res) {
            console.dir(res.headers);
            return res.body
        })
        .then(function(buf) {
            // console.log('\n\n\n***************\n\n\n', buf.toString('ascii'), '\n\n\n***************\n\n\n');
            var options = {
                method: 'POST',
                uri: 'http://localhost:5000/upload_frame',
                formData: {
                    frame: {
                        value: buf,
                        options: {
                            filename: 'frame.jpg',
                            contentType: 'image/jpeg'
                        }
                    }
                }
            };

            return rp(options);
        })
        .catch(function(err) {
            console.log('ERR', err);
        });
};
