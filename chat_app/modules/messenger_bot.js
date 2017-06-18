// Messenger Bot
const request = require('request');
const config = require('config')


const MESSENGER_URI = config.get('messenger_uri')
const PAGE_ACCESS_TOKEN = config.get('page_access_token')


const bot = {
    receivedMessage: function(event) {
        var senderID = event.sender.id;
        var recipientID = event.recipient.id;
        var timeOfMessage = event.timestamp;
        var message = event.message;

        // console.log("Received message for user %d and page %d at %d with message:", senderID, recipientID, timeOfMessage);
        // console.log(JSON.stringify(message));

        var isEcho = message.is_echo;
        var messageId = message.mid;
        var appId = message.app_id;
        var metadata = message.metadata;

        // You may get a text or attachment but not both
        var messageText = message.text;
        var messageAttachments = message.attachments;
        var quickReply = message.quick_reply;

        if (messageText) {
            switch (messageText) {
                case 'sms':
                    this.sendTextMessage(senderID, messageText);
                    break;

                default:
                    request.post({
                        url: config.get('ai_url'),
                        headers: {
                            "content-type": "application/json",
                        },
                        body: JSON.stringify({
                            message: {
                                type: 'text',
                                content: messageText === '' ? 'Ямар үйлдлийн': messageText
                            }
                        })

                    }, function(err, httpResponse, body) {
                        if (err) console.log(err);
                        body = JSON.parse(body);
                        bot.sendTextMessage(senderID, body['message']['content']);

                    });
            }
        } else if (messageAttachments) {
            this.sendTextMessage(senderID, "Message with attachment received");
        }
    },


    receivedPostback: function(event) {
        var senderID = event.sender.id;
        var recipientID = event.recipient.id;
        var timeOfPostback = event.timestamp;


        var payload = event.postback.payload;

        console.log("Received postback for user %d and page %d with payload '%s' " +
            "at %d", senderID, recipientID, payload, timeOfPostback);


        this.sendTextMessage(senderID, "Postback called");
    },

    sendButtonMessage: function(recipientId) {
        var messageData = {
            recipient: {
                id: recipientId
            },
            message: {
                attachment: {
                    type: "template",
                    payload: {
                        template_type: "button",
                        text: "Таны хайж байсан хариулт мөн үү?",
                        buttons: [{
                            type: "postback",
                            title: "Тийм",
                            payload: "yes"
                        }, {
                            type: "postback",
                            title: "Үгүй",
                            payload: "no"
                        }]
                    }
                }
            }
        };

        this.callSendAPI(messageData);
    },

    sendTextMessage: function(recipientId, messageText) {
        var messageData = {
            recipient: {
                id: recipientId
            },
            message: {
                text: messageText,
                metadata: "DEVELOPER_DEFINED_METADATA"
            }
        };

        this.callSendAPI(messageData);
    },
    callSendAPI: function(messageData) {
        request({
            uri: MESSENGER_URI,
            qs: { access_token: PAGE_ACCESS_TOKEN },
            method: 'POST',
            json: messageData

        }, function(error, response, body) {
            if (!error && response.statusCode == 200) {
                var recipientId = body.recipient_id;
                var messageId = body.message_id;

                if (messageId) {
                    console.log("Successfully sent message with id %s to recipient %s",
                        messageId, recipientId);
                } else {
                    console.log("Successfully called Send API for recipient %s",
                        recipientId);
                }
            } else {
                console.error("Failed calling Send API", response.statusCode, response.statusMessage, body.error);
            }
        });
    }
};

module.exports = bot;
