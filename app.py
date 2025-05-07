from flask import Flask, render_template, request, jsonify
import face_recognition
import numpy as np
import cv2
import base64
from datetime import datetime
import os

app = Flask(__name__)

# 🔍 সব পরিচিত মুখ লোড করা
known_encodings = []
known_names = []

for filename in os.listdir("known_faces"):
    if filename.endswith(".jpg"):
        name = os.path.splitext(filename)[0]  # eg: shamim.jpg => shamim
        image = face_recognition.load_image_file(f"known_faces/{filename}")
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)
        else:
            print(f"❌ মুখ খুঁজে পাওয়া যায়নি: {filename}")

@app.route('/')
def index():
    return render_template('index.html')

def save_attendance_to_file(name, time_now):
    with open("attendance.txt", "a") as f:
        f.write(f"{name},{time_now}\n")

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    img_data = base64.b64decode(data['image'].split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # শনাক্তকরণ
    face_locations = face_recognition.face_locations(img_np)
    encodings = face_recognition.face_encodings(img_np, face_locations)

    if not encodings:
        return jsonify({'status': 'fail', 'message': '😕 কোন মুখ পাওয়া যায়নি'})

    for encoding in encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)

        if True in matches:
            best_match_index = np.argmin(face_distances)
            name = known_names[best_match_index]
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_attendance_to_file(name, time_now)
            return jsonify({'status': 'success', 'message': f'✅ {name} - Attendance Marked at {time_now}'})
    
    return jsonify({'status': 'fail', 'message': '❌ মুখ মিললো না কারও সাথে'})


if __name__ == '__main__':
    app.run(debug=True)
