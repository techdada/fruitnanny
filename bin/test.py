import cv2
import time

stream_url = "rtsp://fruitnanny:phr00tnenn.i@localhost:5000/fruitnanny"

cap = cv2.VideoCapture(stream_url) # it can be rtsp or http stream
ret, frame = cap.read()
if ret:
    cv2.imwrite('/tmp/latest.jpg', frame)
    #ret, frame = cap.read()
