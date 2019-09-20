"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cv = require("opencv");
const sleep = require("sleep");
let camera = new cv.VideoCapture("udp://127.0.0.1:5005");
camera.setWidth(512);
camera.setHeight(288);
let window = new cv.NamedWindow("Camera");
let firstFrame;
let frameDelta;
let gray;
let thresh;
sleep.sleep(3);
camera.read((err, frame) => {
    firstFrame = frame;
    firstFrame.cvtColor("CV_BGR2GRAY");
    firstFrame.gaussianBlur([21, 21]);
});
let interval = setInterval(() => {
    camera.read((err, frame) => {
        gray = frame.copy();
        gray.cvtColor("CV_BGR2GRAY");
        gray.gaussianBlur([21, 21]);
        frameDelta = new cv.Matrix();
        frameDelta.absDiff(firstFrame, gray);
        thresh = frameDelta.threshold(25, 255);
        thresh.dilate(2);
        let cnts = thresh.findContours();
        for (let i = 0; i < cnts.size(); i++) {
            if (cnts.area(i) < 500) {
                continue;
            }
            frame.putText("Motion Detected", 10, 20, cv.FONT_HERSHEY_SIMPLEX, [0, 0, 255], 0.75, 2);
        }
        window.show(frame);
        let keyPressed = window.blockingWaitKey(0, 50);
        if (keyPressed === 27) {
            clearInterval(interval);
        }
    });
}, 20);
