import cv2
import os
import numpy as np

def load_face_data(data_folder):
    face_data = {}
    for file_name in os.listdir(data_folder):
        person_name = os.path.splitext(file_name)[0]
        image_path = os.path.join(data_folder, file_name)
        image = cv2.imread(image_path)
        face_data[person_name] = image

    return face_data

def preprocess_face(image):
    resized_image = cv2.resize(image, (160, 160))
    return resized_image

def recognize_faces(test_image, face_data):
    gray_test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_test_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        return None
    known_face_names = list(face_data.keys())
    known_face_resized = {name: preprocess_face(known_face) for name, known_face in face_data.items()}
    for (x, y, w, h) in faces:
        face_roi = test_image[y:y+h, x:x+w]
        recognized_person = "Unknown"
        for name, known_face in known_face_resized.items():
            mse = np.mean((preprocess_face(face_roi) - known_face) ** 2)
            if mse < 500:
                recognized_person = name
                break
        cv2.rectangle(test_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(test_image, recognized_person, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return test_image

if __name__ == "__main__":
    data_folder = "collected_faces" 
    face_data = load_face_data(data_folder)
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        recognized_frame = recognize_faces(frame, face_data)
        if recognized_frame is not None:
            cv2.imshow('Face Recognition', recognized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
