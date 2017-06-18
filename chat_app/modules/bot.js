// Chat bot
const request = require('request');
const config = require('config');
var io = require('socket.io');

module.exports = function(server) {
    io = io(server);
    // Real Time
    io.on('connection', function(socket) {
        setTimeout(function() {
            let msg_data = { 'msg': 'Сайн байна уу танд юугаар туслах уу?', 'bot': 1, 'name': 'Bot' };
            io.emit('reply', JSON.stringify(msg_data));

        }, 2000);

        // Listen
        socket.on('message', function(data) {
            request.post({
                url: config.get('ai_url'),
                headers: {
                    "content-type": "application/json",
                },
                body: JSON.stringify({
                    message: {
                        type: 'text',
                        content: data.msg,
                        time: ''
                    }
                })

            }, function(err, httpResponse, body) {
                if (err) console.log(err);
               
                // console.log("---------------------------");
                // console.log(body);
                // console.log("---------------------------");


                body = JSON.parse(body);
                io.emit('reply', JSON.stringify({ 'time': body['message']['time'], 'msg': body['message']['content'], 'name': 'Bot', 'bot': 1 }));
            });
        });
    });
}
