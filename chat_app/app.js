// Package
const path = require('path');
const express = require('express');
const app = express();
const server = require('http').Server(app);
const bodyParser = require('body-parser');
// const io = require('socket.io')(server);
const session = require('express-session');
const config = require('config');
const request = require('request');

// Bot module
const chat_bot = require('./modules/bot.js')(server);
const messenger_bot = require('./modules/messenger_bot.js');

// Runnnig server on config/default.json -> port_number
server.listen(config.get('port_number'), function() {
    console.log('Running on port: ' + config.get('port_number'))
})

//initialize the session
app.use(session({
    secret: "ubhackathon",
    resave: true,
    saveUninitialized: true
}));

// Body parser 
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

// Static files
app.use('/static', express.static(path.join(__dirname, 'public')));
// Template engine
app.use(express.static(__dirname + '/views'));

// Rounting
const routes_chat = express.Router()
const routes_messenger = express.Router()

require('./routes/app.js')(routes_chat, chat_bot);
require('./routes/messenger.js')(routes_messenger, messenger_bot);

app.use('/', routes_chat);
app.use('/webhook', routes_messenger);
