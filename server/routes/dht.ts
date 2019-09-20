"use strict";

import express = require("express");
import fs = require("fs");
let router = express.Router();

router.get("/current", (req: express.Request, res: express.Response, next: express.NextFunction) => {
    // console.log("On");
    // let temp = Math.random() * (30 - 10) + 10;
    // let hum = Math.random() * 100;
    // let result = { humidity: hum, temperature: temp };
    // res.json(result);
    let jsonText = fs.readFileSync("/tmp/fruitnanny_dht.txt");
    let json = JSON.parse(jsonText.toString());
    res.json(json);

});

export default router;
