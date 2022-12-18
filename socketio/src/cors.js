'use strict'
const cors = require('cors')
exports.main = cors({
  origin: function (origin, callback) {
    callback(null, true)
  },
})

exports.config = {
  cors: {
    origin: function (origin, callback) {

      if (Boolean(origin)) {
        const whitelist = ['https://localhost', 'https://127.0.0.1', 'https://bdata.ca', 'https://biot.bdata.ca']
        let arr = origin.split(".")
        if ((whitelist.indexOf(origin) != -1) || (arr[arr.length - 1] == 'ca' && arr[arr.length - 2] == 'bdata')) {
          callback(null, true)
        } else {
          callback(null, true)
        }

      } else {
        callback(null, true)
      }

    },
    methods: ["GET", "POST"],
    allowedHeaders: "*",
    credentials: true
  }
}
