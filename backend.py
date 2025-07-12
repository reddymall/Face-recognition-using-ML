from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS
import os
import base64
import threading
from image2 import start_recognition, stop_recognition, send_email  # Import send_email function

# Initialize Flask app
app = Flask(__name__,template_folder=r'C:\Project_copy_final\project')
CORS(app)  # Enable Cross-Origin Resource Sharing

# Directory to store trained images
TRAINED_IMAGES_DIR = r"C:\Project_copy_final\trainedimages"
os.makedirs(TRAINED_IMAGES_DIR, exist_ok=True)

# Thread control for recognition
stop_event = threading.Event()


@app.route('/', methods=['Get','Post'])
def home():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train_person():
    """
    Endpoint to capture a person's image from the camera and train it.
    """
    try:
        name = request.json.get('name')
        person_id = request.json.get('id')
        image_data = request.json.get('image')  # Base64 encoded image

        if not name or not person_id or not image_data:
            return jsonify({"message": "Name, ID, and image are required!"}), 400

        # Decode and save the image
        image_filename = f"{name}_{person_id}.jpg"
        image_path = os.path.join(TRAINED_IMAGES_DIR, image_filename)
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_data.split(",")[1]))  # Decode Base64

        return jsonify({"message": f"Image for {name} (ID: {person_id}) successfully trained!"}), 200

    except Exception as e:
        return jsonify({"message": f"Error during training: {str(e)}"}), 500

@app.route('/start', methods=['POST'])
def start_recognition_api():
    """
    Start face recognition.
    """
    global stop_event
    stop_event.clear()
    thread = threading.Thread(target=start_recognition, args=(stop_event,))
    thread.start()
    return jsonify({"message": "Face recognition started successfully!"}), 200

@app.route('/stop', methods=['POST'])
def stop_recognition_api():
    """
    Stop face recognition and send logs via email.
    """
    global stop_event
    stop_event.set()

    # Send email with face logs after stopping recognition
    send_email()

    return jsonify({"message": "Face recognition stopped. Log file sent via email!"}), 200

@app.route('/logs/download', methods=['GET'])
def download_logs():
    """
    Download the face recognition logs.
    """
    LOG_FILE = r"C:\Project_copy_final\face_logs1.xlsx"
    if os.path.exists(LOG_FILE):
        return send_file(LOG_FILE, as_attachment=True, download_name="face_logs.xlsx")
    else:
        return jsonify({"message": "Log file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
