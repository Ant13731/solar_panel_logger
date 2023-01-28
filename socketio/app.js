'use strict'
const app = require('express')()
const server = require('http').createServer(app)
const cors = require("./src/cors.js")
const middlewares = require("./src/middlewares.js")
const { host, port, listener } = require("./src/address.js")
app.use(middlewares)
const io = require("socket.io")(server, cors.config)

io.on("connection", function (socket) {
  socket.on("connect_error", function () {
    console.log(socket.handshake.time + " failed to connect to socket: " + socket.id)
  })
  socket.emit('connect', 'Connected to socketio server')
  console.log(socket.handshake.time + " connected to new socket: " + socket.id)

  socket.on('voltage', data => {
    try {
      if (typeof data === 'object') {
        // Receive voltage data
        const parsed = JSON.stringify(data)
        const jsonObjectParsed = JSON.parse(parsed)
        console.log('============== Parsed Object ==============')
        console.log(parsed)
        console.log(jsonObjectParsed)
        console.log("===========================================")
      }
    } catch (err) {
      console.log("========= Error ===============")
      console.log(err)
      console.log("===============================")
    }
  })
  socket.on('disconnect', (reason) => {
    console.log("disconnected from the socket: " + socket.id)
    console.log(reason)
    if (reason === 'io server disconnect') {
      socket.connect()
    }
  })
})

server.listen(port, host, listener)