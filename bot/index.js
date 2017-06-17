const VT = 'EAADLkEPkylsBAHZAxYxenZC3zeWVBTI0abVA2PaYbLY90rJDBAZChlZAviZCP4ZCI960gDfEmIXq3JXk7xMZCbB8uvSS9HN63MCYi8DgeBtpPPWkgH0X0M6m1k4lAGm8O6fH3UagWKz8B6JD7xGLnwd7xHLkHKFRyRRLZAD8TMpP8wZDZD'

const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


app.get('/', (req, res) => {
        res.send('Hello World')
    })
    /* For Facebook Validation */
app.get('/webhook', (req, res) => {
    if (req.query['hub.mode'] && req.query['hub.verify_token'] === 'ubhackathon') {
        res.status(200).send(req.query['hub.challenge']);
    } else {
        res.status(403).end();
    }
});

/* Handling all messenges */
app.post('/webhook', (req, res) => {
	var data = req.body;
    if (data.object === 'page') {
        // req.body.entry.forEach(function(entry) {
        //     entry.messaging.forEach(function(event) {
        //         if (event.message && event.message.text) {
        //             sendMessage(event);
        //         }
        //         if (event.postback) {
        //             var text = JSON.stringify(event.postback.payload)
        //             console.log(text)
        //             console.log(event.postback)
        //         }
        //     });
        // });
        // res.status(200).end();


        data.entry.forEach(function(pageEntry) {
            var pageID = pageEntry.id;
            var timeOfEvent = pageEntry.time;

            // Iterate over each messaging event
            pageEntry.messaging.forEach(function(messagingEvent) {
                if (messagingEvent.optin) {
                    receivedAuthentication(messagingEvent);
                } else if (messagingEvent.message) {
                    receivedMessage(messagingEvent);
                } else if (messagingEvent.delivery) {
                    receivedDeliveryConfirmation(messagingEvent);
                } else if (messagingEvent.postback) {
                    receivedPostback(messagingEvent);
                } else if (messagingEvent.read) {
                    receivedMessageRead(messagingEvent);
                } else if (messagingEvent.account_linking) {
                    receivedAccountLink(messagingEvent);
                }
            });
        });


    }
});


function sendMessage(event) {
    let sender = event.sender.id;
    let text = event.message.text;

    request({
        url: 'https://graph.facebook.com/v2.6/me/messages',
        qs: { access_token: VT },
        method: 'POST',
        json: {
            recipient: { id: sender },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "Таны хайж байсан хариулт мөн үү?",
                        "buttons": [{
                            "type": "postback",
                            "title": "Тийм",
                            "payload": "yes_payload"
                        }, {
                            "type": "postback",
                            "title": "Үгүй",
                            "payload": "no_payload"
                        }]
                    }
                }
            }
        }
    }, function(error, response) {
        console.log(response)
        if (error) {
            console.log('Error sending message: ', error);
        } else if (response.body.error) {
            console.log('Error: ', response.body.error);
        }
    });
}



/*
	SEND BUTTON
*/
function sendButtonMessage(recipientId) {
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

    callSendAPI(messageData);
}

/*
	RECEIVED POSTBACK
*/

function receivedPostback(event) {
    var senderID = event.sender.id;
    var recipientID = event.recipient.id;
    var timeOfPostback = event.timestamp;


    var payload = event.postback.payload;

    console.log("Received postback for user %d and page %d with payload '%s' " +
        "at %d", senderID, recipientID, payload, timeOfPostback);

    sendTextMessage(senderID, "Postback called");
}

/*
	SEND TEXT
*/

function sendTextMessage(recipientId, messageText) {
    var messageData = {
        recipient: {
            id: recipientId
        },
        message: {
            text: messageText,
            metadata: "DEVELOPER_DEFINED_METADATA"
        }
    };

    callSendAPI(messageData);
}


/*
	SEND READ RECEIPT
*/

function sendReadReceipt(recipientId) {
    console.log("Sending a read receipt to mark message as seen");

    var messageData = {
        recipient: {
            id: recipientId
        },
        sender_action: "mark_seen"
    };

    callSendAPI(messageData);
}


/*
	CALL SEND API
*/

function callSendAPI(messageData) {
    request({
        uri: 'https://graph.facebook.com/v2.6/me/messages',
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


app.listen(3000, function() {
    console.log('Running 3000')
})
