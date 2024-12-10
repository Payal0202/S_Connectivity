from flask import Flask, render_template, Response
import cv2
import mysql.connector
import time
from threading import Thread

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="flask_user",
    password="flask_password",
    database="flask_app_db"
)

cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS CapturedImages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    captured_at DATETIME NOT NULL,
    image LONGBLOB NOT NULL
);
""")
db.commit()

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def capture_frame():
    while True:
        success, frame = camera.read()
        if not success:
            print("Reinitializing camera...")
            camera.release()
            time.sleep(1)
            camera.open(0, cv2.CAP_DSHOW)
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        img_data = buffer.tobytes()
        try:
            cursor.execute("INSERT INTO CapturedImages (timestamp, image) VALUES (NOW(), %s)", (img_data,))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting image: {err}")
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            success, frame = camera.read()
            if not success:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    thread = Thread(target=capture_frame, daemon=True)
    thread.start()
    app.run(debug=True)
