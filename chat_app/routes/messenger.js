const router = require('express').Router();
const config = require('config');
const bot = require('../modules/messenger_bot.js');



router.get('/webhook', (req, res) => {
    if (req.query['hub.mode'] && req.query['hub.verify_token'] === config.get('validation_token')) {
        res.status(200).send(req.query['hub.challenge']);
    } else {
        res.status(403).end();
    }
});


router.post('/webhook', (req, res) => {
    var data = req.body;
    if (data.object === 'page') {

        data.entry.forEach(function(pageEntry) {
            var pageID = pageEntry.id;
            var timeOfEvent = pageEntry.time;

            pageEntry.messaging.forEach(function(messagingEvent) {
                if (messagingEvent.message) {
                    bot.receivedMessage(messagingEvent);
                } else if (messagingEvent.delivery) {
                    // receivedDeliveryConfirmation(messagingEvent);
                } else if (messagingEvent.postback) {
                    bot.receivedPostback(messagingEvent);
                } else if (messagingEvent.read) {
                    // receivedMessageRead(messagingEvent);
                } else if (messagingEvent.account_linking) {
                    // receivedAccountLink(messagingEvent);
                }
            });
        });
    }
});


module.exports = router;
