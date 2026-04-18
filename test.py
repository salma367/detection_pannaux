import torch
import cv2
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import pathlib
import platform

if platform.system() == "Windows":
    pathlib.PosixPath = pathlib.WindowsPath

# 🔥 Charger modèle (léger)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# ⚡ Optimisations
model.conf = 0.4          # seuil de confiance
model.iou = 0.45          # suppression doublons
model.max_det = 10        # limite détections

# 📉 forcer CPU (plus stable sur ton PC)
model.to('cpu')

# 🎥 webcam
cap = cv2.VideoCapture(0)

# 🔥 réduire résolution webcam (très important pour vitesse)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("✅ Webcam démarrée... (Q pour quitter)")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ⚡ resize encore plus rapide (optionnel mais recommandé)
    frame = cv2.resize(frame, (640, 480))

    # 🚀 inference (sans gradient)
    with torch.no_grad():
        results = model(frame)

    # 🎯 afficher résultats
    frame = results.render()[0]

    cv2.imshow("YOLOv5 Optimized", frame)

    # ⛔ quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()