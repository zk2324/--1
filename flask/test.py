from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import img_to_array

app = Flask(__name__)

# Load models and classifiers once at startup
face_cascade = cv2.CascadeClassifier('C:/Users/teohz/Downloads/haarcascade_frontalface_default.xml')
classifier = load_model('C:/Users/teohz/uni_project/model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

@app.route('/')
def index():
    return render_template('Thome.html')

@app.route('/wait')
def wait():
    return render_template('wait.html')

@app.route('/api/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        img_data = base64.b64decode(data['image'].split(',')[1])
        img = Image.open(BytesIO(img_data))
        img = np.array(img)

        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 10)
        
        results = []

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48))

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                prediction = classifier.predict(roi)[0]
                emotion_label = emotion_labels[prediction.argmax()]
                cv2.putText(frame, emotion_label, (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                results.append({
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h),
                    'emotion': emotion_label,
                    'confidence': float(prediction.max())
                })

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
