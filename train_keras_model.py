#!/usr/bin/env python3
"""
Script d'Entraînement Keras (CNN) pour la Reconnaissance de Panneaux
Utilise un dataset synthétique pour démonstration.
"""

import os
import numpy as np
import cv2
import random

# Tentative d'importation de Keras/TensorFlow
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from tensorflow.keras.utils import to_categorical
    from sklearn.model_selection import train_test_split
    HAS_TF = True
except ImportError:
    HAS_TF = False
    print("⚠️ Keras/TensorFlow non trouvé. Le script simulera la structure d'entraînement.")

def generate_synthetic_data(num_samples=1000, img_size=32):
    """Générer des images synthétiques de panneaux de vitesse (30, 50, 80)"""
    X = []
    y = []
    classes = [30, 50, 80]
    
    print(f"📷 Génération de {num_samples} images synthétiques...")
    
    for _ in range(num_samples):
        # Créer un cercle rouge
        img = np.zeros((img_size, img_size, 3), dtype=np.uint8)
        cv2.circle(img, (img_size//2, img_size//2), img_size//2 - 2, (0, 0, 255), -1)
        cv2.circle(img, (img_size//2, img_size//2), img_size//2 - 2, (255, 255, 255), 2)
        
        # Ajouter le texte (nombre)
        class_idx = random.randint(0, len(classes)-1)
        text = str(classes[class_idx])
        
        # Positionnement du texte au centre
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (img_size - text_size[0]) // 2
        text_y = (img_size + text_size[1]) // 2
        
        cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
        
        # Ajouter un peu de bruit et flou pour le réalisme
        noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
        img = cv2.add(img, noise)
        img = cv2.GaussianBlur(img, (3, 3), 0)
        
        X.append(img)
        y.append(class_idx)
        
    return np.array(X), np.array(y)

def train():
    if not HAS_TF:
        print("❌ Erreur: TensorFlow/Keras est nécessaire pour l'entraînement.")
        return

    # 1. Préparation des données
    X, y = generate_synthetic_data(num_samples=2000)
    X = X.astype('float32') / 255.0
    y = to_categorical(y, num_classes=3)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Construction du modèle CNN
    print("\n🏗️ Construction du modèle CNN...")
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(3, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # 3. Entraînement
    print("\n🚀 Démarrage de l'entraînement...")
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
    
    # 4. Sauvegarde
    model_path = "traffic_sign_model.h5"
    model.save(model_path)
    print(f"\n✅ Modèle sauvegardé : {model_path}")

if __name__ == "__main__":
    train()
