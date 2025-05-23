import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Dropout
from tensorflow.keras.layers import Flatten, Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

IMG_WIDTH = 48
IMG_HEIGHT = 48
BATCH_SIZE = 32
EPOCHS = 100
NUM_CLASSES = 7
TRAIN_PATH = '/kaggle/input/fer2013/train'  
TEST_PATH = '/kaggle/input/fer2013/test'   

EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
def load_data(train_path, test_path):
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    

    print("Încărcare date de antrenare...")
    for emotion_idx, emotion in enumerate(EMOTIONS):
        emotion_dir = os.path.join(train_path, emotion)
        
        if not os.path.exists(emotion_dir):
            print(f"Directorul {emotion_dir} nu există!")
            continue
            
        
        for img_file in os.listdir(emotion_dir):
            if img_file.endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(emotion_dir, img_file)
                
                img = tf.keras.preprocessing.image.load_img(
                    img_path, 
                    target_size=(IMG_HEIGHT, IMG_WIDTH),
                    color_mode='grayscale'  
                )
                img_array = tf.keras.preprocessing.image.img_to_array(img)
                
                
                X_train.append(img_array)
                y_train.append(emotion_idx)
    
    print("Încărcare date de testare...")
    for emotion_idx, emotion in enumerate(EMOTIONS):
        emotion_dir = os.path.join(test_path, emotion)
        
        if not os.path.exists(emotion_dir):
            print(f"Directorul {emotion_dir} nu există!")
            continue
            
        for img_file in os.listdir(emotion_dir):
            if img_file.endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(emotion_dir, img_file)
                img = tf.keras.preprocessing.image.load_img(
                    img_path, 
                    target_size=(IMG_HEIGHT, IMG_WIDTH),
                    color_mode='grayscale'  
                )
                img_array = tf.keras.preprocessing.image.img_to_array(img)
                
                
                X_test.append(img_array)
                y_test.append(emotion_idx)
    
    X_train = np.array(X_train, dtype='float32')
    y_train = np.array(y_train)
    X_test = np.array(X_test, dtype='float32')
    y_test = np.array(y_test)
    
    print(f"Număr de imagini de antrenare: {len(X_train)}")
    print(f"Număr de imagini de testare: {len(X_test)}")
    
    y_train = tf.keras.utils.to_categorical(y_train, NUM_CLASSES)
    y_test = tf.keras.utils.to_categorical(y_test, NUM_CLASSES)
    
    return X_train, X_test, y_train, y_test


def cnn_model():
    model = Sequential([
        Conv2D(32, (3, 3), padding='same', input_shape=(IMG_HEIGHT, IMG_WIDTH, 1)),
        Activation('relu'),
        BatchNormalization(),
        Conv2D(32, (3, 3), padding='same'),
        Activation('relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.2),

        Conv2D(64, (3, 3), padding='same'),
        Activation('relu'),
        BatchNormalization(),
        Conv2D(64, (3, 3), padding='same'),
        Activation('relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.2),

        Conv2D(128, (3, 3), padding='same'),
        Activation('relu'),
        BatchNormalization(),
        Conv2D(128, (3, 3), padding='same'),
        Activation('relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.2),

        Conv2D(256, (3, 3), padding='same'),
        Activation('relu'),
        BatchNormalization(),
        Conv2D(256, (3, 3), padding='same'),
        Activation('relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.2),

        Flatten(),
        Dense(512),
        Activation('relu'),
        BatchNormalization(),
        Dropout(0.4),
        Dense(NUM_CLASSES),
        Activation('softmax')
        ])
    
    return model



def train_and_evaluate():
    
    X_train, X_test, y_train, y_test = load_data(TRAIN_PATH, TEST_PATH)
    
    X_train = X_train / 255.0
    X_test = X_test / 255.0
    
    
    datagen = ImageDataGenerator(
        rotation_range=15,            
        width_shift_range=0.1,      
        height_shift_range=0.1,     
        horizontal_flip=True,
        zoom_range=0.1,
        fill_mode='nearest'
    )
    
    datagen.fit(X_train)
    
    model = cnn_model()
    
    
    model.compile(
        optimizer=Adam(learning_rate=0.0005),  
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.summary()
    
 
    checkpoint = ModelCheckpoint(
        'final_emotion_model_48x48_best.keras',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=30,               
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=6,               
        min_lr=1e-6,
        verbose=1
    )
    
    callbacks = [checkpoint, early_stopping, reduce_lr]
    
  
    history = model.fit(
        datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_test, y_test),
        callbacks=callbacks
    )
    
    
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f'\nAcuratețe pe setul de test: {test_acc:.4f}')
    print(f'Loss pe setul de test: {test_loss:.4f}')
    
    
    plot_training_history(history)
    

    model.save('final_emotion_model_48x48_final.keras')
    
    return model, history, X_test, y_test



def plot_training_history(history):
  
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Acuratețea modelului')
    plt.ylabel('Acuratețe')
    plt.xlabel('Epocă')
    plt.legend(['Antrenare', 'Validare'], loc='lower right')
    
   
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Loss-ul modelului')
    plt.ylabel('Loss')
    plt.xlabel('Epocă')
    plt.legend(['Antrenare', 'Validare'], loc='upper right')
    
    plt.tight_layout()
    plt.savefig('training_history_48x48.png')
    plt.show()



def predict_and_visualize(model, X_test, y_test, num_images=5):
    
    indices = np.random.choice(range(len(X_test)), num_images, replace=False)
    
    plt.figure(figsize=(15, 10))
    for i, idx in enumerate(indices):
        
        img = X_test[idx].reshape(1, IMG_HEIGHT, IMG_WIDTH, 1)
        pred = model.predict(img)[0]
        pred_class = np.argmax(pred)
        true_class = np.argmax(y_test[idx])
        
        
        plt.subplot(1, num_images, i+1)
        plt.imshow(X_test[idx].reshape(IMG_HEIGHT, IMG_WIDTH), cmap='gray')
        plt.title(f'Adevărat: {EMOTIONS[true_class]}\nPrezis: {EMOTIONS[pred_class]}\nConfidență: {pred[pred_class]:.2f}')
        plt.axis('off')
    
    plt.savefig('prediction_samples_48x48.png')
    plt.show()  



def main():
    
    model, history, X_test, y_test = train_and_evaluate()
    
    predict_and_visualize(model, X_test, y_test)

if __name__ == "__main__": 
    main()      