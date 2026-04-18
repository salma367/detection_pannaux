import cv2
import numpy as np
import os
import time
from sklearn.neighbors import KNeighborsClassifier

dataset_path = "datasetSmartCities"

# =========================
# HOG DESCRIPTOR
# =========================
hog = cv2.HOGDescriptor(
    _winSize=(32, 32),
    _blockSize=(16, 16),
    _blockStride=(8, 8),
    _cellSize=(8, 8),
    _nbins=9
)

# =========================
# LOAD DATASET
# =========================
def load_dataset():
    data = []
    labels = []

    for label in os.listdir(dataset_path):
        folder = os.path.join(dataset_path, label)

        if not os.path.isdir(folder):
            continue

        for file in os.listdir(folder):
            img = cv2.imread(os.path.join(folder, file), 0)
            img = cv2.resize(img, (32, 32))

            features = hog.compute(img).flatten()
            data.append(features)
            labels.append(int(label))

    return np.array(data), np.array(labels)

X, y = load_dataset()

# =========================
# TRAIN MODEL
# =========================
knn = KNeighborsClassifier(n_neighbors=4)
knn.fit(X, y)

print("Model trained with", len(X), "samples")

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

last_time = 0
COOLDOWN = 0.5  # seconds

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    display_frame = frame.copy()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # RED MASK
    lower1 = np.array([0, 100, 80])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 100, 80])
    upper2 = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower1, upper1) + cv2.inRange(hsv, lower2, upper2)
    mask = cv2.GaussianBlur(mask, (9, 9), 2)

    circles = cv2.HoughCircles(
        mask,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=60,
        param1=100,
        param2=25,
        minRadius=15,
        maxRadius=80
    )

    current_time = time.time()

    if circles is not None and (current_time - last_time > COOLDOWN):
        circles = np.uint16(np.around(circles))

        for (x, y, r) in circles[0, :]:
            cv2.circle(display_frame, (x, y), r, (0, 255, 0), 2)

            y1, y2 = max(0, y-r), min(frame.shape[0], y+r)
            x1, x2 = max(0, x-r), min(frame.shape[1], x+r)

            roi = frame[y1:y2, x1:x2]

            if roi.size != 0:
                last_time = current_time

                # 64x64 (processing)
                roi_64 = cv2.resize(roi, (64, 64))

                # =========================
                # CLASSIFICATION
                # =========================
                gray = cv2.cvtColor(roi_64, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, (32, 32))

                feature = hog.compute(gray).flatten().reshape(1, -1)

                prediction = knn.predict(feature)[0]
                probs = knn.predict_proba(feature)[0]
                confidence = np.max(probs)

                # =========================
                # PRINT TERMINAL
                # =========================
                print("==========")
                print(f"Prediction: {prediction}")
                print(f"Confidence: {confidence:.2f}")
                print("==========")

                # =========================
                # DISPLAY RESULT
                # =========================
                text = f"{prediction}" if confidence > 0.6 else "Unknown"
                color = (0, 255, 0) if confidence > 0.6 else (0, 0, 255)

                cv2.putText(display_frame, text, (x - 20, y - r - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                break

    # SHOW LIVE FEED WITH RESULT
    cv2.imshow("Live Camera", display_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()