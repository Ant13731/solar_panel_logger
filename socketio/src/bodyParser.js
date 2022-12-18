'use strict'
const express = require('express')
exports.urlEncoded = express.urlencoded({ extended: true })

exports.json = express.json()