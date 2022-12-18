'use strict'
const bodyParser = require("./bodyParser.js")
const cors = require("./cors.js")

module.exports = [
    cors.main, bodyParser.json, bodyParser.urlEncoded,
]

