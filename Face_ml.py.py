import cv2
import face_recognition
import numpy as np
import os
import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime

# Dictionary storing ID, Name, and Image_File (without extension)
person_details = {
    "keerthana_543": {"ID": "101", "Name": "Keerthana"},
    "souimage": {"ID": "513", "Name": "Soubhagya"},
    "sravani": {"ID": "565", "Name": "Sravani"},
    "gnana_prasuna": {"ID": "558", "Name": "Gnana Prasuna"},
    "swathi": {"ID": "505", "Name": "Swathi"},
    "Madhavi": {"ID": "566", "Name": "Madhavi"},
}

# Paths
LOG_FILE = r"C:\Project_copy_final\face_logs1.xlsx"
FOLDER_PATH = r"C:\Project_copy_final\trainedimages"

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  # Use "smtp.office365.com" for Outlook
SMTP_PORT = 587
SENDER_EMAIL = "sravanireddyyarasu123@gmail.com"  # Replace with your email
SENDER_PASSWORD = "syezdtcueshorztm"  # Generate an app password if using Gmail
RECEIVER_EMAIL = "reddymallukeerthana@gmail.com"  # Replace with recipient's email

# Ensure Excel log file exists
def ensure_log_file():
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=["ID", "Name", "Date", "Time"])
        df.to_excel(LOG_FILE, index=False, engine='openpyxl')
        print("✅ Created new log file: face_logs1.xlsx")

# Send email with logs
def send_email():
    """Send face logs via email when recognition stops."""
    try:
        if not os.path.exists(LOG_FILE):
            print("❌ Log file not found. Skipping email.")
            return

        msg = EmailMessage()
        msg["Subject"] = "Face Recognition Logs"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg.set_content("Attached is the face recognition log.")

        with open(LOG_FILE, "rb") as f:
            msg.add_attachment(f.read(), maintype="application",
                               subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               filename="face_logs.xlsx")

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Load trained faces
def load_trained_faces(folder_path):
    trained_faces = {}
    if not os.path.exists(folder_path):
        print("❌ Error: Directory does not exist!")
        return {}

    for file in os.listdir(folder_path):
        if file.endswith(".jpg") or file.endswith(".png"):
            image_path = os.path.join(folder_path, file)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                trained_faces[file.split(".")[0]] = encodings[0]
    print(f"✅ Loaded {len(trained_faces)} trained faces.")
    return trained_faces

# Compare captured face with trained faces
def recognize_face(known_faces, face_encoding):
    names = list(known_faces.keys())
    encodings = list(known_faces.values())

    matches = face_recognition.compare_faces(encodings, face_encoding)
    face_distances = face_recognition.face_distance(encodings, face_encoding)

    if any(matches):
        best_match_index = np.argmin(face_distances)
        return names[best_match_index]
    return "Unknown"

# Track logged persons for the session
logged_persons = set()

# Log detected faces
def log_face_detection(face_name):
    global logged_persons

    if face_name in logged_persons:
        return  # Skip duplicate entries

    logged_persons.add(face_name)

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if face_name in person_details:
        person_info = person_details[face_name]
        face_id = person_info["ID"]
        face_name = person_info["Name"]
    else:
        face_id = "Unknown"
        face_name = "Unknown"

    new_entry = pd.DataFrame([[face_id, face_name, date, time]], 
                              columns=["ID", "Name", "Date", "Time"])

    try:
        if os.path.exists(LOG_FILE):
            existing_data = pd.read_excel(LOG_FILE, engine='openpyxl')
            updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
        else:
            updated_data = new_entry
    except Exception as e:
        print(f"❌ Error updating log file: {e}")
        return

    updated_data.to_excel(LOG_FILE, index=False, engine='openpyxl')
    print(f"✅ Logged: {face_name} at {time} on {date}")

# Real-time face recognition
def start_recognition(stop_event):
    ensure_log_file()
    global trained_faces
    trained_faces = load_trained_faces(FOLDER_PATH)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Ensure camera initialization
    if not cap.isOpened():
        print("❌ Error: Camera not accessible")
        return

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Failed to capture image")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            face_name = recognize_face(trained_faces, face_encoding)

            log_face_detection(face_name)

            color = (0, 255, 0) if face_name != "Unknown" else (0, 0, 255)
            display_text = f"ID: {person_details.get(face_name, {}).get('ID', 'Unknown')} | Name: {face_name}"

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, display_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Stop Recognition Function
def stop_recognition():
    print("Stopping recognition (handled by stop_event).")
    send_email()  # Automatically send email after stopping recognition
