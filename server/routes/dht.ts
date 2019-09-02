"use strict";

import express = require("express");
import * as cp from "child_process";
import * as config from "../../fruitnanny_config";
let router = express.Router();

router.get("/current", (req: express.Request, res: express.Response, next: express.NextFunction) => {
    // console.log("On");
    // let temp = Math.random() * (30 - 10) + 10;
    // let hum = Math.random() * 100;
    // let result = { humidity: hum, temperature: temp };
    // res.json(result);
console.log("Sensor Type: " + config.sensor_type);
    if (config.sensor_type == undefined) config.sensor_type = "dht22";
    let dhtscript = "bin/" + config.sensor_type + ".py";
    cp.exec(dhtscript, (err, stdout, stderr) => {
        let values = stdout.split(" ");
        let t = values[0];
        let h = values[1];
        let result = { humidity: h, temperature: t };
        res.json(result);
    });
});

export default router;
