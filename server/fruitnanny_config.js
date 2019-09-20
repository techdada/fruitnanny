"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const path = require("path");
let jsonTextConfig = fs.readFileSync(path.resolve(__dirname, "../fruitnanny_config.json"));
let config = JSON.parse(jsonTextConfig.toString());
module.exports = config;
