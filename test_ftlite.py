import cv2
import numpy as np
import tensorflow as tf

# =========================
# LOAD MODEL
# =========================
interpreter = tf.lite.Interpreter(model_path="best_int8.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_index = input_details[0]['index']
output_index = output_details[0]['index']

input_dtype = input_details[0]['dtype']

# 🔥 tes classes (IMPORTANT)
labels = ["30", "50", "60", "80", "STOP", "END", "RED", "GREEN", "ORANGE"]

IMG_SIZE = 320

# =========================
# IMAGE TEST
# =========================
img_path = "70.png"   # <-- change ici
frame = cv2.imread(img_path)

if frame is None:
    print("❌ Image introuvable")
    exit()

h0, w0 = frame.shape[:2]

# =========================
# PREPROCESS
# =========================
img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))

if input_dtype == np.float32:
    img_input = img.astype(np.float32) / 255.0
else:
    img_input = img.astype(np.uint8)

img_input = np.expand_dims(img_input, axis=0)

# =========================
# INFERENCE
# =========================
interpreter.set_tensor(input_details[0]['index'], img_input)
interpreter.invoke()

output = interpreter.get_tensor(output_details[0]['index'])

# =========================
# POSTPROCESS YOLO
# =========================
pred = output[0].T  # (2100, 12)

boxes = pred[:, :4]
obj = pred[:, 4]
cls = pred[:, 5:]

class_ids = np.argmax(cls, axis=1)
scores = obj * np.max(cls, axis=1)

# =========================
# RESULT TERMINAL
# =========================
detected = False

for i in range(len(scores)):
    if scores[i] > 0.5:

        label = labels[class_ids[i]]
        print(f"🔥 Détection: {label} | confiance: {scores[i]:.2f}")

        detected = True

if not detected:
    print("❌ Aucun panneau détecté")