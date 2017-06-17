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
        let base = new db.Base({ q: data.q, a: data.a }).save(function(err) {
            if (err) {
                console.log(data.id + '. ' + data.q + ' - ' + data.a)
            }
        })
    }).on('end', function() {
        console.log('Base done.')
    })
}

function addDataContra(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
        let contra = new db.Contra({ q: data.q, a: data.a }).save(function(err) {
            if (err) {
                console.log(data.id + '. ' + data.q + ' - ' + data.a)
            }
        })
    }).on('end', function() {
        console.log('Contra done.')

    })

}

function addDataCrm(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
        let crm = new db.Crm({ q: data.q, a: data.a }).save(function(err) {
            if (err) {
                console.log(data.id + '. ' + data.q + ' - ' + data.a)
            }
        })
    }).on('end', function() {
        console.log('Crm done.')
    })
}

function addDataFinance(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
        let fina = new db.Finance({ q: data.q, a: data.a }).save(function(err) {
            if (err) {
                console.log(data.id + '. ' + data.q + ' - ' + data.a)
            }
        })
    }).on('end', function() {
        console.log('Finance done.')
        

    })
}

function addDataHrm(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
        let hrm = new db.Hrm({ q: data.q, a: data.a }).save(function(err) {
            if (err) {
                console.log(data.id + '. ' + data.q + ' - ' + data.a)
            }
        })
    }).on('end', function() {
        console.log('Hrm done.')
    })
}

function addDataScm(url) {
    fs.createReadStream(url).pipe(stream).on('data', function(data) {
        let scm = new db.Scm({ q: data.q, a: data.a }).save(function(err) {
            if (err) {
                console.log(data.id + '. ' + data.q + ' - ' + data.a)
            }
        })
    }).on('end', function() {
        console.log('Scm done.')
    })
}

addDataBase('./data/base.csv')
// addDataContra('./data/contract.csv')
// addDataCrm('./data/crm.csv')
// addDataFinance('./data/finance.csv')
// addDataHrm('./data/hrm.csv')
// addDataScm('./data/scm.csv')
