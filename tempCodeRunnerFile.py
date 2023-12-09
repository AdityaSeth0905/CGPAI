import cv2
import json
import face_recognition
import os
import time

# Open the webcam
video_capture = cv2.VideoCapture(0)

# Initialize variables to track if a person is found
person_found = False

# Specify the directory to save the captured images
image_directory = r"C:\Users\adity\OneDrive\Desktop\work\GPAI\WebFrameFeedPics"