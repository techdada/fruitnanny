"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require("express");
const fs = require("fs");
let router = express.Router();
router.get("/current", (req, res, next) => {
    let jsonText = fs.readFileSync("/tmp/fruitnanny_dht.txt");
    let json = JSON.parse(jsonText.toString());
    res.json(json);
});
exports.default = router;
