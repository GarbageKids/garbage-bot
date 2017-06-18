const db = require('../db_builder/db.js');

module.exports = function(router, bot) {
    router.get('/', function(req, res) {
        res.sendFile('index.html');
    });
}
