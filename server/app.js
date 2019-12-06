"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const config = require("./fruitnanny_config");
const custom_button_1 = require("./routes/custom_button");
const dht_1 = require("./routes/dht");
//const detection = require("./camera/detection_oc");
const express = require("express");
const light_1 = require("./routes/light");
let app = express();
/*function init_detection() {
    console.log("Init detection");
    detection.run({
        onDetectedMotion: () => {
            console.log("### initCapture()");
        },
        onError: () => {
            setTimeout(init_detection, 500);
        },
    });
}*/
app.set("view engine", "ejs");
app.set("views", "views");
app.use("/public", express.static("public"));
app.get("/", (req, res, next) => {
    res.render("index", { config });
});
app.get("/settings", (req, res, next) => {
    res.render("settings", { config });
});
app.use("/api/light", light_1.default);
app.use("/api/dht", dht_1.default);
app.use("/api/custom_button", custom_button_1.default);
app.listen(7000, () => {
    console.log("Fruitnanny app listening on port 7000!");
});
//init_detection();
