# press the live window then press c to capture then y to confirm prediction or n to deny and enter the right value
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
# LOAD DATASET (HOG FEATURES)
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

            features = hog.compute(img).flatten()  # 🔥 HOG here

            data.append(features)
            labels.append(int(label))

    return np.array(data), np.array(labels)

X, y = load_dataset()

# Train model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

print("Model trained with", len(X), "samples")

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # ROI (replace later with your detection)
    roi = frame[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7)]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (32, 32))

    # 🔥 HOG FEATURE
    feature = hog.compute(gray).flatten().reshape(1, -1)

    prediction = knn.predict(feature)[0]

    cv2.putText(frame, f"Pred: {prediction}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("ROI", roi)

    key = cv2.waitKey(1)

    # =========================
    # INTERACTIVE LEARNING
    # =========================
    if key == ord('c'):  # capture
        print(f"Prediction: {prediction}")
        user_input = input("Confirm? (y/n): ")

        if user_input.lower() == 'y':
            label = prediction
        else:
            label = input("Enter correct label: ")

        # Save image
        save_folder = os.path.join(dataset_path, str(label))
        os.makedirs(save_folder, exist_ok=True)

        count = len(os.listdir(save_folder))
        cv2.imwrite(f"{save_folder}/{count}.png", gray)

        print("Saved to dataset")

        # 🔥 Retrain model
        X, y = load_dataset()
        knn.fit(X, y)

        print("Model updated")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()