#USAGE: python3 camera_algorithm.py --room "[room name]"

# Importing libraries
import cv2
import imutils
import requests
from time import sleep, gmtime, strftime
import argparse
from datetime import datetime

# Read video input from the camera
cap = cv2.VideoCapture(0)

# Create the haar cascade
bodyCascade = cv2.CascadeClassifier("haarcascade_upperbody.xml")

# Argument Parser
ap = argparse.ArgumentParser()
ap.add_argument("-r", "--room", required=True, help="room name")
args = vars(ap.parse_args())

# declaring variables
roomName = args["room"]
availability = ""
lastA= ""
start_hour = ""
end_hour = ""

try:
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        frame = imutils.resize(frame, width=min(400, frame.shape[1]))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect bodies in the image
        bodies = bodyCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Update availability when persons are detected
        if (len(bodies) > 0):
            availability = "Occupied"
            if start_hour == "":
                start_hour = datetime.now().strftime("%H:%M:%S")
        else:
            availability = "Unoccupied"
            end_hour = datetime.now().strftime("%H:%M:%S")

        # Figure out when to update room status
        if (lastA != availability):
            lastA = availability
            # print("Found {0} persons!".format(len(bodies)))
            # print ("Sending..")
            requests.post('[API Gateway Link]', json={"name": roomName, "state":"Online", "availability":availability})
        
        # Figure out when to send logs
        if start_hour != "" and end_hour != "" and availability == "Unoccupied":
            date = strftime("%A %d %B %Y")
            requests.post('[API Gateway Link]', json={"room": roomName , "date": date,"trigger_hour": start_hour, "trigger_end_hour": end_hour, "number_of_persons": len(bodies)})
            print (start_hour + " | " + end_hour)
            start_hour = ""
            end_hour = ""

        # Draw a rectangle around the bodies
        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Add some sleep so you don't fry your Raspberry
        sleep(0.5)

# If the code stops for some reason, update Raspberry status on the site and also change availability to "Unknown"
except:
    requests.post('[API Gateway Link]', json={"name": roomName, "state":"Offline", "availability":"Unknown"})
    # When everything's done, release the capture
    cap.release()
    cv2.destroyAllWindows()
