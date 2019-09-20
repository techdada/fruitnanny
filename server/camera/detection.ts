import PiMotion = require("node-pi-motion");
import _ = require("lodash");

let camera;
let closing = false;

const defaultOptions = {
    autorestart: false,
    night: false,
    onDetectedMotion: null,
    onError: null,
    onReady: null,
    sensitivity: 100,
    sleep: 0.5, // sec
    threshold : 10,
    throttle: 0,
    verbose: false,
};

export function run(opts: { onReady?: any; onDetectedMotion?: any; onError?: any; }) {
    opts = opts || {};
    opts = Object.assign(defaultOptions, opts);

    closing = false;

    camera = new PiMotion(pimotionOptions(opts));

    camera.on("ready", () => {
        if (closing) { return; }
        console.log("Camera ready to detect motions");
        if (opts.onReady) { opts.onReady(); }
    });

    camera.on("DetectedMotion", () => {
        if (closing) { return; }
        console.log("Motion detected!");
        if (opts.onDetectedMotion) { opts.onDetectedMotion(); }
    });

    camera.on("error", ( err ) => {
        if (closing) { return; }
        console.log("Camera detection error:");
        console.error(err);
        if (opts.onError) { opts.onError(); }
    });
}

export function close() {
    if (closing) { return; }
    if (camera) {
        console.log( "Detection closing..." );
        camera.close();
        closing = true;

    } else {
        console.log( "Detection: Nothing to close" );
    }
}

/**
 * Pick options except nulls
 */
function pimotionOptions( opts: { onReady?: any; onDetectedMotion?: any; onError?: any; } ) {
    opts = opts || {};
    const excludeParams = [
        "onReady",
        "onDetectedMotion",
        "onError",
    ];
    return _.pickBy(opts, ( val, key ) => {
        return excludeParams.indexOf(key) < 0;
    });
}
