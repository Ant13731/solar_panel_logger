'use strict'
const path = require("path")
let { host, port } = require("./server.json")
exports.host = "127.0.0.1"


exports.port = port
exports.address = `http://${module.exports.host}:${module.exports.port}`


exports.listener = function () {
    console.log(`server listening at ${module.exports.address}`)
}