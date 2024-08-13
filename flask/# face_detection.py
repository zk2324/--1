import cv2
import numpy as np
import json
from datetime import datetime
from keras.models import load_model
from keras.preprocessing.image import img_to_array

def get_current_time_str():
    return datetime.now().strftime("%Y%m%d_%H%M")

def initialize_video_capture(output_path):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))
    return cap, out

def load_models():
    face_cascade = cv2.CascadeClassifier('C:/Users/teohz/Downloads/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('C:/Users/teohz/uni_project/Face_recongnition/Face_recongnition/face.yml')
    classifier = load_model('C:/Users/teohz/uni_project/model.h5')
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    return face_cascade, recognizer, classifier, emotion_labels

def process_frame(frame, face_cascade, recognizer, classifier, emotion_labels, name, data):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        person_name = name.get(str(idnum), '???') if confidence < 60 else '???'
        label_position = (x, y - 10)
        cv2.putText(frame, person_name, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48))

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            prediction = classifier.predict(roi)[0]
            emotion_label = emotion_labels[prediction.argmax()]
            cv2.putText(frame, emotion_label, (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            data.append({
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h),
                'name': person_name,
                'emotion': emotion_label,
                'confidence': float(prediction.max())
            })
        else:
            cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame, data

def main():
    now = get_current_time_str()
    output_video_file = f'C:/Users/teohz/uni_project/video/output_video_{now}.avi'
    output_json_file = f'C:/Users/teohz/uni_project/emoji_result/emotion_results_{now}.json'
    
    cap, out = initialize_video_capture(output_video_file)
    face_cascade, recognizer, classifier, emotion_labels = load_models()
    
    name = {
        '1': 'Moonbyul',
        '2': 'Alice',
        '3': 'Ze Kai'
    }
    
    data = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法读取摄像头影像，请确认摄像头是否连接正常。")
            break
        
        frame, data = process_frame(frame, face_cascade, recognizer, classifier, emotion_labels, name, data)
        
        out.write(frame)
        cv2.imshow('Emotion and Recognition Detector', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    with open(output_json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"数据已写入 {output_json_file}")
    print(f"视频已保存到 {output_video_file}")

if __name__ == '__main__':
    main()