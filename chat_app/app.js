// Package
const path = require('path');
const express = require('express');
const app = express();
const server = require('http').Server(app);
const bodyParser = require('body-parser');
const io = require('socket.io')(server);
const session = require('express-session');

// Runnnig server on 3000
server.listen(8000)

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

// ROUTING
const router_app = require('./routes/app.js');
const router_messenger = require('./routes/messenger.js');
app.use('/', router_app);
app.use('/', router_messenger);