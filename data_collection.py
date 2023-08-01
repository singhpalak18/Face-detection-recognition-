import cv2
import os
from tkinter import filedialog, Tk
from PIL import Image

output_folder = "collected_faces"
os.makedirs(output_folder, exist_ok=True)

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def capture_from_webcam():

    ret, frame = video_capture.read()
    cv2.putText(frame, "Press 's' to save the image or 'q' to go back.", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1)
    cv2.imshow('Data Collection', frame)

    key = cv2.waitKey(0) & 0xFF

    if key == ord('s'):
    
        person_name = input("Enter the person's name: ")

        person_name = person_name.strip().lower()

        image_path = os.path.join(output_folder, f"{person_name}.jpg")
        cv2.imwrite(image_path, frame)
        print(f"Saved face image for {person_name}.")

    elif key == ord('q'):
        return

def upload_image():
    Tk().withdraw()  
    file_path = filedialog.askopenfilename(title="Select Face Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
         image = Image.open(file_path)
        person_name = input("Enter the person's name: ")
        person_name = person_name.strip().lower()
        image_path = os.path.join(output_folder, f"{person_name}.jpg")
        image.save(image_path)
        print(f"Saved face image for {person_name}.")
while True:
    print("Choose an option:")
    print("1. Capture face image from webcam")
    print("2. Upload face image")
    print("3. Quit")
    choice = input("Enter option number (1, 2, or 3): ")

    if choice == '1':
        capture_from_webcam()
    elif choice == '2':
        upload_image()
    elif choice == '3':
        break
video_capture.release()
cv2.destroyAllWindows()
