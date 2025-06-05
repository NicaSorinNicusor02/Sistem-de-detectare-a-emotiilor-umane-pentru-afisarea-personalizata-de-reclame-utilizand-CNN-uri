import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import cv2
import numpy as np
import tensorflow as tf
load_model = tf.keras.models.load_model
from collections import Counter
import show_ads_frame
from show_ads_frame import process_neural_output, EMOTION_TO_CATEGORY, emotion_vector

show_ads_frame.start_emotion_analysis()
show_ads_frame.start_ads_display()

model = load_model('final_emotion_model_48x48_best.keras')
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
labels_dict = {0:'angry', 1:'disgust', 2:'fear', 3:'happy', 4:'neutral', 5:'sad', 6:'surprise'}

def get_current_dominant_emotion():
    if not emotion_vector:
        return show_ads_frame.get_dominant_emotion()
    current_counts = Counter(emotion_vector)
    if current_counts:
        dominant, _ = current_counts.most_common(1)[0]
        return dominant
    return show_ads_frame.get_dominant_emotion()

def create_info_header():
    real_time_dominant = get_current_dominant_emotion()
    official_dominant = show_ads_frame.get_dominant_emotion()
    header_height = 240
    header_width = 1000
    header = np.ones((header_height, header_width, 3), dtype=np.uint8) * 240
    title_font_size = 0.65
    text_font_size = 0.55
    small_font_size = 0.5
    cv2.putText(header, "INFORMATII DESPRE RECLAMA AFISATA:", 
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, title_font_size, (0, 0, 150), 2)
    
    cv2.putText(header, f"Emotia dominanta (reclama): {official_dominant}", 
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, text_font_size, (0, 0, 150), 1)
    
    prev_categories = EMOTION_TO_CATEGORY.get(official_dominant, ['categorie5', 'categorie9', 'categorie10'])
    prev_categories_text = ", ".join(prev_categories)
    cv2.putText(header, f"Categoria (reclama): {prev_categories_text}", 
                (20, 85), cv2.FONT_HERSHEY_SIMPLEX, text_font_size, (0, 0, 150), 1)
    
    cv2.putText(header, "INFORMATII DESPRE COLECTAREA ACTUALA:", 
                (20, 120), cv2.FONT_HERSHEY_SIMPLEX, title_font_size, (0, 0, 0), 2)

    cv2.putText(header, f"Emotia dominanta (actuala): {real_time_dominant}", 
                (20, 150), cv2.FONT_HERSHEY_SIMPLEX, text_font_size, (0, 0, 0), 1)

    categories = EMOTION_TO_CATEGORY.get(real_time_dominant, ['categorie5', 'categorie9', 'categorie10'])
    categories_text = ", ".join(categories)
    cv2.putText(header, f"Categoria (actuala): {categories_text}", 
                (20, 175), cv2.FONT_HERSHEY_SIMPLEX, text_font_size, (0, 0, 0), 1)
    
    cv2.putText(header, "Clasament emotii detectate:", 
                (20, 210), cv2.FONT_HERSHEY_SIMPLEX, title_font_size, (0, 0, 0), 2)
    current_counts = Counter(emotion_vector)
    emotions = list(EMOTION_TO_CATEGORY.keys())
    x_pos = 80
    for emotion in emotions[:3]:
        count = current_counts.get(emotion, 0)
        text = f"{emotion}: {count}"
        cv2.putText(header, text, 
                    (x_pos, 235), cv2.FONT_HERSHEY_SIMPLEX, small_font_size, (0, 0, 0), 1)
        x_pos += 120
        
    x_pos = 450
    for emotion in emotions[3:5]:
        count = current_counts.get(emotion, 0)
        text = f"{emotion}: {count}"
        cv2.putText(header, text, 
                    (x_pos, 235), cv2.FONT_HERSHEY_SIMPLEX, small_font_size, (0, 0, 0), 1)
        x_pos += 120
    
    x_pos = 700
    for emotion in emotions[5:]:
        count = current_counts.get(emotion, 0)
        text = f"{emotion}: {count}"
        cv2.putText(header, text, 
                    (x_pos, 235), cv2.FONT_HERSHEY_SIMPLEX, small_font_size, (0, 0, 0), 1)
        x_pos += 140
    return header

video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Eroare: Nu s-a putut deschide camera")
    exit()
print("Camera s-a deschis cu succes")

while True:
    ret, frame = video.read()
    if not ret:
        print("Eroare la citirea frame-ului")
        break
    info_header = create_info_header()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 3)
    
    for x, y, w, h in faces:
        sub_face_img = gray[y:y+h, x:x+w]
        resized = cv2.resize(sub_face_img, (48, 48))
        normalize = resized / 255.0
        reshaped = np.reshape(normalize, (1, 48, 48, 1))
        result = model.predict(reshaped)
        label = np.argmax(result, axis=1)[0]
        detected_emotion = labels_dict[label].lower()
        
        process_neural_output(detected_emotion)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, labels_dict[label], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    if frame.shape[1] != info_header.shape[1]:
        frame = cv2.resize(frame, (info_header.shape[1], int(frame.shape[0] * info_header.shape[1] / frame.shape[1])))
    combined_frame = np.vstack((info_header, frame))
    cv2.imshow("Detectare emotii", combined_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
