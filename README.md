# Face-recognition-using-ML
# Real-Time Face Recognition System 🚀

This project is a real-time face recognition system built with **Python**, **Flask**, **OpenCV**, and **face_recognition**. It allows you to train new faces using a webcam, perform real-time face detection and recognition, and log recognized faces to an Excel file. The logs can be automatically sent via email when recognition stops.

---

## 📂 Project Structure

├── backend.py # Flask backend API
├── Face_ml.py.py # Face recognition core logic
├── index.html # Simple frontend to interact with the backend
├── trainedimages/ # Folder to store trained images
├── face_logs1.xlsx # Auto-generated log file for face detections

---

## ✨ Features

✅ Train new faces using your webcam  
✅ Real-time face recognition  
✅ Save recognition logs to Excel  
✅ Send logs automatically via email  
✅ Download logs from the web interface

---

## ⚙️ How it Works

1. **Train a Face:**  
   - Click **"Train Unknown Person"**  
   - Allow camera access and enter name & ID  
   - Capture an image and train

2. **Start Recognition:**  
   - Click **"Start Recognition"** to launch real-time detection  
   - The system compares detected faces with the trained images

3. **Stop Recognition:**  
   - Click **"Stop Recognition"**  
   - The system stops the camera and sends the log via email

4. **Download Logs:**  
   - Click **"View Logs"** to download the Excel file with detection details

---

## 🛠️ Technologies Used

- Python
- Flask
- OpenCV
- face_recognition
- Pandas
- HTML, CSS, JavaScript (vanilla)

---

## 🔒 Important Note

- Update the **sender email**, **receiver email**, and **app password** in `Face_ml.py.py`:
  ```python
  SENDER_EMAIL = "your_email@gmail.com"
  SENDER_PASSWORD = "your_app_password"
  RECEIVER_EMAIL = "recipient_email@gmail.com"
Getting Started
1️⃣ Install Requirements
bash
Copy
Edit
pip install flask flask-cors opencv-python face_recognition pandas openpyxl
2️⃣ Run the Backend
bash
Copy
Edit
python backend.py
3️⃣ Open the Frontend
Open index.html in your browser.
Make sure the backend is running at http://127.0.0.1:5000.

📬 Log Emailing
When you stop the recognition:

The backend sends the face_logs1.xlsx to the configured recipient.

📑 License
This project is for educational purposes only.

🙌 Authors
Keerthana

Team Members: Soubhagya, Sravani, Gnana Prasuna, Swathi, Madhavi

💡 Tips
Press Q in the OpenCV window to quit recognition manually.

Ensure your webcam is accessible.

Keep trainedimages/ organized with unique names.
