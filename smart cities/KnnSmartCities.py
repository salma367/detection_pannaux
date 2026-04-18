#click on the live window first
#press s to capture ou 7awlou tjibou sign exactly wsst l cadre sghir
#press q to exit 
import cv2
import numpy as np
import os
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
#jrbou tbdlou n_neighbors!!
print("Model trained with", len(X), "samples")

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(0)

last_capture = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # ROI
    roi = frame[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7)]

    display_frame = frame.copy()

    cv2.rectangle(display_frame,
                  (int(w*0.3), int(h*0.3)),
                  (int(w*0.7), int(h*0.7)),
                  (255, 255, 0), 2)

    cv2.imshow("Live", display_frame)
    cv2.imshow("ROI", roi)

    key = cv2.waitKey(1) & 0xFF

    # =========================
    # SCREENSHOT MODE
    # =========================
    if key == ord('s'):
        print("Captured!")

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (32, 32))

        feature = hog.compute(gray).flatten().reshape(1, -1)

        prediction = knn.predict(feature)[0]
        probs = knn.predict_proba(feature)[0]
        confidence = np.max(probs)

        result_img = roi.copy()

        if confidence > 0.6:
            text = f"{prediction} ({confidence:.2f})"
            color = (0, 255, 0)
        else:
            text = "Unknown"
            color = (0, 0, 255)

        cv2.putText(result_img, text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("Captured Result", result_img)

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()