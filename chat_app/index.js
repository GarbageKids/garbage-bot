// require('./db.js')
// var data = require('./data.js')()
// console.log(data)


const express = require('express')
var bodyParser = require('body-parser')
const app = express()
app.use(bodyParser.json({ type: 'application/*+json' }))

app.get('/', function(req, res) {
    res.send('Hello World!')
})

app.listen(3000, function() {
    console.log('listening on port 3000!')
})
