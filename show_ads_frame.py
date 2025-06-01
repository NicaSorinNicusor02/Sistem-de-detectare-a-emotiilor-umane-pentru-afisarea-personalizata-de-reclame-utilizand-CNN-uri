import os
import sys
import django
import time
import threading
from collections import Counter
from tkinter import Tk, Label, Frame
from PIL import Image, ImageTk
import random
from website_ads.models import Ad
import threading

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_ads.settings')
django.setup()

emotion_vector = []
last_added_emotion = None
last_emotion_counts = Counter()

current_emotion = 'neutral'
previous_emotion = 'neutral'

EMOTION_TO_CATEGORY = {
    'angry': ['categorie4', 'categorie1'],
    'disgust': ['categorie7', 'categorie8'],
    'fear': ['categorie2', 'categorie7', 'categorie10'],
    'happy': ['categorie3', 'categorie8', 'categorie9'],
    'neutral': ['categorie5', 'categorie10', 'categorie9'],
    'sad': ['categorie1', 'categorie2'],
    'surprise': ['categorie6', 'categorie11'],
}

def process_neural_output(emotion_label):
    global last_added_emotion
    emotion_label = emotion_label.lower()
    if emotion_label != last_added_emotion:
        add_emotion(emotion_label)
        last_added_emotion = emotion_label

def add_emotion(emotion):
    global emotion_vector, last_emotion_counts
    emotion_vector.append(emotion)
    last_emotion_counts = Counter(emotion_vector)
    print(f"Emotie adaugata: {emotion}. Total emotii: {len(emotion_vector)}")
    print(f"Clasament curent: {dict(last_emotion_counts)}")

def analyze_emotions():
    global emotion_vector, last_emotion_counts, previous_emotion
    if not emotion_vector:
        print("Vectorul de emotii este gol, nimic de analizat!")
        return None
    emotion_counts = Counter(emotion_vector)
    last_emotion_counts = emotion_counts
    most_common_emotion, count = emotion_counts.most_common(1)[0]
    print(f"Clasament final emotii: {emotion_counts}")
    print(f"Emotia dominanta: {most_common_emotion} ({count} aparitii)")
    return most_common_emotion

def emotion_analyzer_task():
    global current_emotion, previous_emotion, last_added_emotion
    while True:
        print("\n===== START CICLU NOU DE ANALIZA (5 secunde) =====")
        print("Colectare emotii pentru 5 secunde...")
        time.sleep(5)
        print("\n=== ANALIZAM VECTORUL DE EMOTII ===")
        dominant_emotion = analyze_emotions()

        if dominant_emotion:
            previous_emotion = current_emotion
            current_emotion = dominant_emotion
            print(f"Emotia dominanta actualizata: {current_emotion} (anterior: {previous_emotion})")
        emotion_vector.clear()
        last_added_emotion = None
        print(f"Vector de emotii resetat.")
        print("===== SFARSIT CICLU DE ANALIZA =====\n")

def get_dominant_emotion():
    global current_emotion
    return current_emotion

def get_previous_dominant_emotion():
    global previous_emotion
    return previous_emotion

def start_ads_display():
    ads_thread = threading.Thread(target=show_ads_window)
    ads_thread.daemon = True
    ads_thread.start()
    print("Afisarea reclamelor a inceput")

def start_emotion_analysis():
    global analyzer_thread
    analyzer_thread = threading.Thread(target=emotion_analyzer_task)
    analyzer_thread.daemon = True
    analyzer_thread.start()
    print("Analiza emotiilor a inceput")

def show_ads_window():
    global current_emotion
    try:
        import imageio
        from PIL import Image, ImageTk
        import numpy as np
        import time
        imageio_available = True
    except ImportError:
        print("Biblioteca imageio nu este instalată")
        imageio_available = False
        
    root = Tk()
    root.title("Afisare Reclame Bazate pe Emotii")
    window_width = 1100
    window_height = 700
    root.geometry(f"{window_width}x{window_height}")
    
    ad_label = Label(root)
    ad_label.pack(fill="both", expand=True)
    video_reader = None
    is_playing_video = False
    start_time = 0
    frame_count = 0
    total_frames = 0
    fps = 0

    def display_video_frame():
        nonlocal video_reader, is_playing_video, start_time, frame_count, total_frames, fps
        if not is_playing_video or video_reader is None:
            return
        try:
            elapsed_time = time.time() - start_time
            target_frame = int(elapsed_time * fps)
            if target_frame >= total_frames:
                print(f"Video terminat. Frame-uri afisate: {frame_count}/{total_frames}")
                stop_video()
                root.after(100, update_ad)
                return
            if target_frame <= frame_count:
                root.after(1, display_video_frame)
                return
            try:
                video_reader.set_image_index(target_frame)
                frame = video_reader.get_next_data()
                frame_count = target_frame
            except (IndexError, RuntimeError) as e:
                print(f"Eroare la citirea frame-ului {target_frame}: {e}")
                frame_count += 1
                root.after(1, display_video_frame)
                return
            frame_image = Image.fromarray(frame)
            frame_image = frame_image.resize((window_width, window_height), Image.LANCZOS)
            frame_tk = ImageTk.PhotoImage(frame_image)
            ad_label.config(image=frame_tk)
            ad_label.image = frame_tk
            delay = int(1000/fps/3)
            root.after(delay, display_video_frame)
            
        except Exception as e:
            print(f"Eroare in timpul redarii video: {e}")
            stop_video()
            root.after(100, update_ad)
    
    def play_video(video_path):
        nonlocal video_reader, is_playing_video, start_time, frame_count, total_frames, fps
        if not imageio_available:
            print("Imageio nu este disponibil. Nu se poate reda videoclipul.")
            return False
        try:
            stop_video()
            print(f"Incepem redarea videoclipului: {video_path}")
            video_reader = imageio.get_reader(video_path)
            meta_data = video_reader.get_meta_data()
            fps = meta_data.get('fps', 30)
            duration = meta_data.get('duration', 0)
            try:
                total_frames = int(duration * fps)
            except:
                try:
                    total_frames = video_reader.count_frames()
                except:
                    total_frames = 1000
            print(f"Date video: FPS={fps}, durata={duration}s, frame-uri totale={total_frames}")

            frame_count = 0
            is_playing_video = True
            start_time = time.time()
            display_video_frame()
            return True
        except Exception as e:
            print(f"Eroare la initierea redarii video: {e}")
            stop_video()
            return False

    def stop_video():
        nonlocal video_reader, is_playing_video
        if video_reader is not None:
            try:
                video_reader.close()
            except:
                pass
            video_reader = None
        is_playing_video = False
    
    def update_ad():
        stop_video()
        all_ads = list(Ad.objects.all())
        all_location_ads = []
        for ad in all_ads:
            if ad.user.city == 'bucurestisector6' and ad.user.shopping_center == 'afi_cotroceni':
                all_location_ads.append(ad)
        if not all_location_ads:
            ad_label.config(image=None, text="Nu există reclame disponibile")
            root.after(5000, update_ad)
            return
        categories = EMOTION_TO_CATEGORY.get(current_emotion, ['categorie5', 'categorie9', 'categorie10'])
        emotion_filtered_ads = []
        for ad in all_location_ads:
            if ad.category in categories:
                emotion_filtered_ads.append(ad)
        if emotion_filtered_ads:
            ads_to_use = emotion_filtered_ads
        else:
            ads_to_use = all_location_ads

        selected_ad = random.choice(ads_to_use)
        if hasattr(selected_ad, 'video') and selected_ad.video and selected_ad.video.name and imageio_available:
            video_path = selected_ad.video.path
            info_text = f"Categorie: {selected_ad.category}"
            ad_label.config(text=info_text, compound="bottom")
            if play_video(video_path):
                return
        if hasattr(selected_ad, 'image') and selected_ad.image and selected_ad.image.name:
            image_path = selected_ad.image.path
            try:
                img = Image.open(image_path)
                img = img.resize((window_width, window_height), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                ad_label.config(image=img_tk)
                ad_label.image = img_tk
                info_text = f"Categorie: {selected_ad.category}"
                ad_label.config(text=info_text, compound="bottom")
            except Exception as e:
                print(f"Eroare la incarcarea imaginii: {e}")
                ad_label.config(image=None, text=f"Categorie: {selected_ad.category}")
        else:
            ad_label.config(image=None, text=f"Categorie: {selected_ad.category}")

        root.after(5000, update_ad)

    update_ad()
    def check_key(event):
        if event.char == 'q':
            root.destroy()
    root.bind('<Key>', check_key)
    root.mainloop()
