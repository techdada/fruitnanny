"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const config = require("../../fruitnanny_config");
const express = require("express");
const cp = require("child_process");
let router = express.Router();
router.get("/current", (req, res, next) => {
    let dhtscript = "bin/dht22.py";
    if (config.sensor_type == "dht11") dhtscript="bin/dht11.py";

    cp.exec(dhtscript, (err, stdout, stderr) => {
        let values = stdout.split(" ");
        let t = values[0];
        let h = values[1];
        let result = { humidity: h, temperature: t };
        res.json(result);
    });
});
exports.default = router;
