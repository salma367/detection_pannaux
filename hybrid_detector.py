import cv2
import numpy as np
import tensorflow as tf

# =========================
# LOAD TFLITE MODEL
# =========================
interpreter = tf.lite.Interpreter(model_path="best_int8.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_index = input_details[0]["index"]
output_index = output_details[0]["index"]

# Labels (adapter selon ton entraînement)
labels = [
    "30",
    "50",
    "60",
    "80",
    "STOP",
    "END_LIMIT",
    "RED_LIGHT",
    "GREEN_LIGHT",
    "ORANGE_LIGHT"
]

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

print("✅ Webcam démarrée... Appuie sur Q pour quitter")

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()

    if not ret:
        break

    display_frame = frame.copy()

    # =========================
    # HSV CONVERSION
    # =========================
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # =========================
    # RED MASK
    # =========================
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = mask1 + mask2

    # =========================
    # MORPHOLOGY
    # =========================
    kernel = np.ones((3, 3), np.uint8)
    red_mask = cv2.morphologyEx(
        red_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # =========================
    # FIND CONTOURS
    # =========================
    contours, _ = cv2.findContours(
        red_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # =========================
    # LOOP OVER OBJECTS
    # =========================
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area < 300:
            continue

        perimeter = cv2.arcLength(cnt, True)

        if perimeter == 0:
            continue

        circularity = 4 * np.pi * area / (perimeter * perimeter)

        # Garde seulement objets presque circulaires
        if circularity < 0.6:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        roi = frame[y:y+h, x:x+w]
        
        if roi.size == 0:
            continue

        # =========================
        # PREPROCESS ROI
        # =========================
        roi_input = cv2.resize(roi, (320, 320))

        roi_input = np.expand_dims(roi_input, axis=0).astype(np.uint8)

        # =========================
        # TFLITE INFERENCE
        # =========================
        interpreter.set_tensor(input_index, roi_input)
        interpreter.invoke()

        prediction = interpreter.get_tensor(output_index)[0]

        best_i = np.argmax(prediction[:, 4])  # objectness score

        class_id = np.argmax(prediction[best_i][5:])
        confidence = prediction[best_i][4]

        label = labels[class_id]

        # seuil confiance
        if confidence > 0.6:
            cv2.rectangle(
                display_frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                display_frame,
                f"{label} ({confidence:.2f})",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.imshow("Hybrid Detection", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()