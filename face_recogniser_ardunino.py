import cv2
import pickle
import serial
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime

# Define the function to send an email
def send_email(frame):
    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['Subject'] = 'Person Detected'
        msg['From'] = 'omsagar250403@gmail.com'
        msg['To'] = "sagarmishra250403@gmail.com"
        
        # Get current date and time
        now = datetime.now()
        formatted_date_time = now.strftime("%d/%m/%Y %H:%M:%S")

        # Email body
        body = f'<strong>A person has been detected by your webcam at {formatted_date_time}.</strong>'
        msg.attach(MIMEText(body, 'html'))

        # Save the frame as an image
        cv2.imwrite('image.jpg', frame)

        # Attach image to the email
        with open('image.jpg', 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name='image.jpg')
        msg.attach(image)

        # Connect to SMTP server and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('omsagar250403@gmail.com', 'enkn zzvr onta qumy')
            server.sendmail('omsagar250403@gmail.com', "sagarmishra250403@gmail.com", msg.as_string())

        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)

# Define the rest of your code
currentname = "unknown"
encodingsP = "encodings.pickle"
cascade = "haarcascade_frontalface_default.xml"

print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

fps = FPS().start()

ser = serial.Serial('COM4', 9600)
time.sleep(2)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                       minNeighbors=5, minSize=(30, 30),
                                       flags=cv2.CASCADE_SCALE_IMAGE)

    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

            if currentname != name:
                currentname = name
                print(currentname)
                ser.write(currentname.encode())
        else:
            # If no match found, consider the face as "Unknown"
            if currentname != "Unknown":
                currentname = "Unknown"
                print(currentname)
                ser.write(currentname.encode())
                # Call send_email function
                send_email(frame)

        names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    .8, (0, 255, 255), 2)

    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
ser.close()
