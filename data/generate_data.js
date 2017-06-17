// File
const csv = require('csv-parser')
const fs = require('fs')
const stream = csv(['id', 'q', 'a'])
const db = require('./db.js')

// Clear db
db.removeAll()

// Add data functions
function addDataBase(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
    	new db.Base({q: data.q, a: data.a}).save(function(err) {
    		if(err) throw err;
    	})
    }).on('end', function() {
    	console.log('Base done.')
    })
}

function addDataContra(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
    	new db.Contra({q: data.q, a: data.a}).save(function(err) {
    		if(err) throw err;
    	})
    }).on('end', function() {
    	console.log('Contra done.')
    })
   
}

function addDataCrm(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
    	new db.Crm({q: data.q, a: data.a}).save(function(err) {
    		if(err) throw err;
    	})
    }).on('end', function() {
    	console.log('Crm done.')
    })
}

function addDataFinance(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
    	new db.Finance({q: data.q, a: data.a}).save(function(err) {
    		if(err) throw err;
    	})
    }).on('end', function() {
    	console.log('Finance done.')
    })
}

function addDataHrm(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
    	new db.Hrm({q: data.q, a: data.a}).save(function(err) {
    		if(err) throw err;
    	})
    }).on('end', function() {
    	console.log('Hrm done.')
    })
}

function addDataScm(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
    	new db.Scm({q: data.q, a: data.a}).save(function(err) {
    		if(err) throw err;
    	})
    }).on('end', function() {
    	console.log('Scm done.')
    })
}

addDataBase('./data/base.csv')
// addDataContra('./data/contract.csv')
// var c = addDataCrm('./data/crm.csv')
// var d = addDataFinance('./data/finance.csv')
// var e = addDataHrm('./data/hrm.csv')
// var f = addDataScm('./data/scm.csv')