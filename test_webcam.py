import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'

import cv2
import numpy as np

#from keras.models import load_model ; folosind asa aveam erori
import tensorflow as tf
load_model = tf.keras.models.load_model

from collections import Counter
import show_ads_frame
from show_ads_frame import process_neural_output, EMOTION_TO_CATEGORY, emotion_vector

show_ads_frame.start_emotion_analysis()#porneste analiza emotiilor
show_ads_frame.start_ads_display()# porneste afiaarea reclamelor

#model = load_model('emotion_model.keras')
#model = load_model('emotion_model_final_13.04.keras')
#model = load_model('emotion_model_best_14.04.keras')
#model = load_model('emotion_model_gray_best.keras')
#model = load_model('emotion_model_48x48_best.keras') #doar acesta afiseaza bine
model = load_model('final_emotion_model_48x48_best.keras') #si acesta afiseaza bine

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
labels_dict = {0:'anger', 1:'disgust', 2:'fear', 3:'happy', 4:'neutral', 5:'sad', 6:'surprise'}

# functie pentru a determina emotia dominanta din vectorul curent
def get_current_dominant_emotion():
    if not emotion_vector:
        return show_ads_frame.get_dominant_emotion()  # folosim ultima emotie dominanta daca vectorul e gol
    
    # calculam emotia cu cele mai multe aparitii
    current_counts = Counter(emotion_vector)
    if current_counts:
        dominant, _ = current_counts.most_common(1)[0]
        return dominant
    
    return show_ads_frame.get_dominant_emotion()

#functie pentru a crea header-ul cu informatii despre emotii
def create_info_header():
    real_time_dominant = get_current_dominant_emotion() # obtinem emotia dominanta din vectorul curent pentru afisare in timp real
    official_dominant = show_ads_frame.get_dominant_emotion() # obtinem emotia dominanta curenta, pentru care se afiseaza reclama
    # cream un canvas alb pentru header
    header_height = 240
    header_width = 1000
    header = np.ones((header_height, header_width, 3), dtype=np.uint8) * 240  # fundal gri deschis
    
    # dimensiuni font-uri
    title_font_size = 0.65
    text_font_size = 0.55
    small_font_size = 0.5
    
    #sectiunea pentru emotia anterioara (cea pentru care se afiseaza reclama)
    cv2.putText(header, "INFORMATII DESPRE RECLAMA AFISATA:", 
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, title_font_size, (0, 0, 150), 2)
    
    # emotia dominanta anterioara = cea care este folosita pentru reclama actuala
    cv2.putText(header, f"Emotia dominanta (reclama): {official_dominant}", 
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, text_font_size, (0, 0, 150), 1)
    
    #categoriile emotiei anterioare
    prev_categories = EMOTION_TO_CATEGORY.get(official_dominant, ['categorie5', 'categorie9', 'categorie10'])
    prev_categories_text = ", ".join(prev_categories)
    cv2.putText(header, f"Categoria (reclama): {prev_categories_text}", 
                (20, 85), cv2.FONT_HERSHEY_SIMPLEX, text_font_size, (0, 0, 150), 1)
    
    #sectiunea pentru emotia curenta
    cv2.putText(header, "INFORMATII DESPRE COLECTAREA ACTUALA:", 
                (20, 120), cv2.FONT_HERSHEY_SIMPLEX, title_font_size, (0, 0, 0), 2)
    
    # emotia dominanta, calculata in timp real din vectorul curent
    cv2.putText(header, f"Emotia dominanta (actuala): {real_time_dominant}", 
                (20, 150), cv2.FONT_HERSHEY_SIMPLEX, text_font_size, (0, 0, 0), 1)
    
    # categoriiile bazate pe emotia dominanta in timp real
    categories = EMOTION_TO_CATEGORY.get(real_time_dominant, ['categorie5', 'categorie9', 'categorie10'])
    categories_text = ", ".join(categories)
    cv2.putText(header, f"Categoria (actuala): {categories_text}", 
                (20, 175), cv2.FONT_HERSHEY_SIMPLEX, text_font_size, (0, 0, 0), 1)
    
    # titlu clasament centrat in partea de jos
    cv2.putText(header, "Clasament emotii detectate:", 
                (20, 210), cv2.FONT_HERSHEY_SIMPLEX, title_font_size, (0, 0, 0), 2)
    
    #obtinem clasamentul curent direct din vectorul de emotii
    current_counts = Counter(emotion_vector)
    
    # clasament emotii - imprrtit pe doua randuri pentru a evita suprapunerea
    emotions = list(EMOTION_TO_CATEGORY.keys())
    
    #pozitionez primul set de emotii (primele 3)
    x_pos = 80
    for emotion in emotions[:3]:
        count = current_counts.get(emotion, 0)
        text = f"{emotion}: {count}"
        cv2.putText(header, text, 
                    (x_pos, 235), cv2.FONT_HERSHEY_SIMPLEX, small_font_size, (0, 0, 0), 1)
        x_pos += 120
    
    # pozitionez al doilea set de emotii (urmatoarele 2)
    x_pos = 450
    for emotion in emotions[3:5]:
        count = current_counts.get(emotion, 0)
        text = f"{emotion}: {count}"
        cv2.putText(header, text, 
                    (x_pos, 235), cv2.FONT_HERSHEY_SIMPLEX, small_font_size, (0, 0, 0), 1)
        x_pos += 120
    
    # pozitionez ultimele emotii
    x_pos = 700
    for emotion in emotions[5:]:
        count = current_counts.get(emotion, 0)
        text = f"{emotion}: {count}"
        cv2.putText(header, text, 
                    (x_pos, 235), cv2.FONT_HERSHEY_SIMPLEX, small_font_size, (0, 0, 0), 1)
        x_pos += 140
    
    return header

#pornim camera
video = cv2.VideoCapture(0)

#verific daca camera s-a deschis corect
if not video.isOpened():
    print("Eroare: Nu s-a putut deschide camera")
    exit()

print("Camera s-a deschis cu succes")

# bucla principala pentru procesarea video
while True:
    ret, frame = video.read()
    if not ret:
        print("Eroare la citirea frame-ului")
        break

    # cream header-ul cu informatii
    info_header = create_info_header()
    
    # procesare pentru detectarea emotiilor
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 3)
    
    for x, y, w, h in faces:
        sub_face_img = gray[y:y+h, x:x+w]
        resized = cv2.resize(sub_face_img, (48, 48))
        normalize = resized / 255.0
        reshaped = np.reshape(normalize, (1, 48, 48, 1))
        result = model.predict(reshaped)
        label = np.argmax(result, axis=1)[0]
        # obtin numele emotiei
        detected_emotion = labels_dict[label].lower()
        
        # trimitem emotia detectata către sistemul de reclame
        # logica de verificare pentru emotii duplicate este in show_ads_frame.py
        process_neural_output(detected_emotion)
        
        # aplic chenarele pe fata
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, labels_dict[label], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # redimensionam frame-ul pentru a se potrivi cu latimea header-ului
    if frame.shape[1] != info_header.shape[1]:
        frame = cv2.resize(frame, (info_header.shape[1], int(frame.shape[0] * info_header.shape[1] / frame.shape[1])))
    
    #combinam header-ul cu frame-ul camerei
    combined_frame = np.vstack((info_header, frame))
    
    #afisam imaginea combinata
    cv2.imshow("Detectare emotii", combined_frame)
    
    #iesim cu tasta 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# eliberam resursele
video.release()
cv2.destroyAllWindows()