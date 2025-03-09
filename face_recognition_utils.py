import cv2
import face_recognition
import os
import numpy as np
import pickle

# Create a directory for storing images
image_dir = "static/students/"
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

def capture_image(student_id, student_name):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        img_path = f"{image_dir}{student_id}_{student_name}.jpg"
        cv2.imwrite(img_path, frame)
        cam.release()
        cv2.destroyAllWindows()
        return img_path
    return None

def encode_faces():
    known_face_encodings = []
    known_face_names = []

    print(image_dir)
    # Load existing encodings if available
    if os.path.exists("models/face_encodings.pkl"):
        with open("models/face_encodings.pkl", "rb") as f:
            known_face_encodings, known_face_names = pickle.load(f)

    print("Encoding faces from:", image_dir)

    for filename in os.listdir(image_dir):
        image_path = os.path.join(image_dir, filename)

        # Load and encode face
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)

        if len(encoding) > 0:
            new_encoding = encoding[0]

            # Check if the new face is already encoded
            for existing_encoding in known_face_encodings:
                matches = face_recognition.compare_faces([existing_encoding], new_encoding)
                if True in matches:
                    print(f"Error: Face in {filename} is already registered!")
                    return "Error: Duplicate face detected"

            known_face_encodings.append(encoding[0])
            known_face_names.append(filename.split(".")[0])

    with open("models/face_encodings.pkl", "wb") as f:
        pickle.dump((known_face_encodings, known_face_names), f)
    return "Registration successfull."

def recognize_face(frame):
    with open("models/face_encodings.pkl", "rb") as f:
        known_face_encodings, known_face_names = pickle.load(f)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            matched_index = matches.index(True)
            name = known_face_names[matched_index]

        return name  # Return recognized student name
    return None
