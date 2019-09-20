import fs = require("fs");
import path = require("path");
let jsonTextConfig = fs.readFileSync(path.resolve(__dirname, "../fruitnanny_config.json"));
let config = JSON.parse(jsonTextConfig.toString());
/*let config = {
    "baby_name": "Matthew",
    "baby_birthday": "2016-03-15",
    "temp_unit": "C",
    "sensor_type": "dht11"
}*/

module.exports = config;
