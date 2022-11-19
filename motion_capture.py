from imutils.video import VideoStream
import argparse
import time
import imutils
import cv2
import webbrowser
import osascript

ap = argparse.ArgumentParser()

ap.add_argument("-a", "--min-area", type=int, default=300, help="minimum area size")
args = vars(ap.parse_args())


vs = VideoStream(src=0).start()
time.sleep(2.0)
firstFrame = None
i = 0

while True:
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Safe"
	if frame is None:
		break
	frame = imutils.resize(frame, width=500)

	roi = frame[0:80, 40:220]
	gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	if firstFrame is None:
		firstFrame = gray
		continue

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	for c in cnts:
		if cv2.contourArea(c) < args["min_area"]:
			continue
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 1)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
		text = "Shit"
		if cv2.contourArea(c) > 0:
			i=1

	cv2.putText(roi, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

	cv2.imshow('Cap', roi)
	# cv2.imshow('Frame', frame)
	
	# cv2.imshow("Thresh", thresh)
	# cv2.imshow("Frame Delta", frameDelta)

	
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break
	if i > 0:
		break
target_volume = 0
vol = "set volume output volume " + str(0)
osascript.osascript(vol)
webbrowser.open('https://www.scribbr.com/category/research-paper/', new=2)
vs.stop()
cv2.destroyAllWindows()