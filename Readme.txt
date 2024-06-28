# Facial Recognition System - Main.py

## Introduction
This project is a facial recognition system implemented in Python using OpenCV and face_recognition libraries. It provides functionalities for detecting and recognizing faces from live video streams or static images.

## Requirements
- Python 3.6 or higher
- OpenCV (cv2)
- face_recognition
- imutils
- pickle
- time
- serial (for Arduino integration, optional)

## Usage
1. Ensure that your webcam is connected to your system.
2. Connect your Arduino board to the COM4 port of your system.
3. Upload the necessary Arduino sketch to your Arduino board (if using Arduino integration).
4. Navigate to the directory "src" containing the `Main.py` file.
5. Run the `Main.py` file using Python:

python Main.py

6. The program will start capturing live video from your webcam and perform facial recognition.
7. If any known faces are detected, their names will be displayed on the screen. If an unknown face is detected, an email notification will be sent to the owner (configured in the script), and a signal will be sent to the Arduino board to trigger an action (if Arduino integration is enabled).
8. Press `q` to exit the program.

## Configuration
- To configure email notifications, edit the `send_email()` function in the `Main.py` file and provide your email credentials.
- Modify the `encodings.pickle` file to include encodings of known faces.

## Supported Platforms
- Linux
- macOS
- Windows

## Arduino Integration
- Connect your Arduino board to the COM4 port of your system.
- Upload the Arduino sketch provided in the `Arduino` folder to your Arduino board.
- Ensure that the `serial` library is installed in your Python environment for communication with the Arduino board.
- Modify the `Main.py` file to include the necessary code for sending signals to the Arduino board (if required).

## Acknowledgments
- This project is based on tutorials and resources from OpenCV and face_recognition documentation.

**Note:** Change the images folder as images are not included in this repository. You can add your images to the "image_data" folder and then train your model and run the program accordingly.
