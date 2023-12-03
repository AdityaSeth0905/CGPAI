import cv2
from customtkinter import *
import tkinter as tk
from PIL import Image, ImageTk

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)
        label.config(image=img)
        label.image = img
    root.after(10, update_frame)

cap = cv2.VideoCapture(0)  # 0 represents the default camera (usually the built-in webcam)

root = CTk()
root.title("Login")
label = tk.Label(root)
label.pack()

update_frame()

root.mainloop()

# Release the webcam and close the OpenCV window when the Tkinter window is closed
cap.release()
cv2.destroyAllWindows()
