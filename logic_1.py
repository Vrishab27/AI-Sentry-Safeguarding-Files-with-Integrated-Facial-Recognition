#logic_1.py
import cv2
import face_recognition
import pickle
from cryptography.fernet import Fernet
import os
import subprocess
import time

def get_fernet_key():
    key_file = 'fernet.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as file:
            file.write(key)
    return Fernet(key)

cipher_suite = get_fernet_key()

def encrypt_data(data):
    return cipher_suite.encrypt(data)

def decrypt_data(data):
    return cipher_suite.decrypt(data)

def save_encodings(encodings):
    with open('face_encodings.pkl', 'wb') as f:
        encrypted_data = encrypt_data(pickle.dumps(encodings))
        f.write(encrypted_data)

def load_encodings():
    try:
        with open('face_encodings.pkl', 'rb') as f:
            encrypted_data = f.read()
            return pickle.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, EOFError):
        return {}

face_encodings = load_encodings()

def capture_face_images():
    cap = cv2.VideoCapture(0)
    print("Capturing face images. Press 'c' to capture.")
    captured_faces = []
    while len(captured_faces) < 5:
        ret, frame = cap.read()
        if not ret:
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        cv2.imshow('Capture Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            face_locations = face_recognition.face_locations(rgb_frame)
            if face_locations:
                face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                captured_faces.append(face_encoding)
                print("Face captured.")
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return captured_faces

def add_or_train_face(file_path):
    if not file_path:
        print("No file selected.")
        return
    face_encs = capture_face_images()
    if face_encs:
        face_encodings[file_path] = face_encs
        save_encodings(face_encodings)
        print("Face added/trained successfully.")

def unlock_file_folder(file_path):
    if not file_path or file_path not in face_encodings:
        print("File not locked or no face trained.")
        return False

    print("Attempting to unlock. Look at the camera.")
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    while True:
        if time.time() - start_time > 10:  # 10-second timeout
            print("Face not recognized.")
            cap.release()
            cv2.destroyAllWindows()
            return False

        ret, frame = cap.read()
        if not ret:
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        cv2.imshow('Unlock File/Folder', frame)
        face_locs = face_recognition.face_locations(rgb_frame)
        if face_locs:
            current_face_enc = face_recognition.face_encodings(rgb_frame, face_locs)[0]
            if any(face_recognition.compare_faces(face_encodings[file_path], current_face_enc, tolerance=0.6)):
                print("Face matched, file unlocked.")
                cap.release()
                cv2.destroyAllWindows()
                open_file(file_path)
                return True
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return False

def open_file(file_path):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        else:  # macOS, Linux, and other Unix
            opener = 'open' if os.name == 'mac' else 'xdg-open'
            subprocess.run([opener, file_path])
    except Exception as e:
        print(f"Error opening file: {e}")

# import cv2
# import face_recognition
# import pickle
# from cryptography.fernet import Fernet
# import os
# import subprocess
# import time

# def get_fernet_key():
#     key_file = 'fernet.key'
#     if os.path.exists(key_file):
#         with open(key_file, 'rb') as file:
#             key = file.read()
#     else:
#         key = Fernet.generate_key()
#         with open(key_file, 'wb') as file:
#             file.write(key)
#     return Fernet(key)

# cipher_suite = get_fernet_key()

# def encrypt_data(data):
#     return cipher_suite.encrypt(data)

# def decrypt_data(data):
#     return cipher_suite.decrypt(data)

# def save_encodings(encodings):
#     with open('face_encodings.pkl', 'wb') as f:
#         encrypted_data = encrypt_data(pickle.dumps(encodings))
#         f.write(encrypted_data)

# def load_encodings():
#     try:
#         with open('face_encodings.pkl', 'rb') as f:
#             encrypted_data = f.read()
#             return pickle.loads(decrypt_data(encrypted_data))
#     except (FileNotFoundError, EOFError):
#         return {}

# face_encodings = load_encodings()

# def capture_face_images():
#     cap = cv2.VideoCapture(0)
#     print("Capturing face images. Press 'c' to capture.")
#     captured_faces = []
#     while len(captured_faces) < 5:
#         ret, frame = cap.read()
#         if not ret:
#             continue
#         cv2.imshow('Capture Face', frame)
#         if cv2.waitKey(1) & 0xFF == ord('c'):
#             face_locations = face_recognition.face_locations(frame)
#             if face_locations:
#                 face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
#                 captured_faces.append(face_encoding)
#                 print("Face captured.")
#         elif cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()
#     return captured_faces

# def add_or_train_face(file_path):
#     if not file_path:
#         print("No file selected.")
#         return
#     face_encs = capture_face_images()
#     if face_encs:
#         face_encodings[file_path] = face_encs
#         save_encodings(face_encodings)
#         print("Face added/trained successfully.")

# def unlock_file_folder(file_path):
#     if not file_path or file_path not in face_encodings:
#         print("File not locked or no face trained.")
#         return False

#     print("Attempting to unlock. Look at the camera.")
#     cap = cv2.VideoCapture(0)
#     start_time = time.time()
#     while True:
#         if time.time() - start_time > 10:  # 10-second timeout
#             print("Face not recognized.")
#             cap.release()
#             cv2.destroyAllWindows()
#             return False

#         ret, frame = cap.read()
#         if not ret:
#             continue
#         cv2.imshow('Unlock File/Folder', frame)
#         face_locs = face_recognition.face_locations(frame)
#         if face_locs:
#             current_face_enc = face_recognition.face_encodings(frame, face_locs)[0]
#             if any(face_recognition.compare_faces(face_encodings[file_path], current_face_enc, tolerance=0.6)):
#                 print("Face matched, file unlocked.")
#                 cap.release()
#                 cv2.destroyAllWindows()
#                 open_file(file_path)
#                 return True
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()
#     return False

# def open_file(file_path):
#     try:
#         if os.name == 'nt':  # Windows
#             os.startfile(file_path)
#         else:  # macOS, Linux, and other Unix
#             opener = 'open' if os.name == 'mac' else 'xdg-open'
#             subprocess.run([opener, file_path])
#     except Exception as e:
#         print(f"Error opening file: {e}")
