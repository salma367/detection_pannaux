from ultralytics import YOLO
import cv2

model1 = YOLO("yolov8n.pt")
model2 = YOLO("best14.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    r1 = model1.predict(frame, verbose=False)[0]
    r2 = model2.predict(frame, verbose=False)[0]

    img1 = r1.plot()
    img2 = r2.plot()

    # fusion simple (choix du meilleur)
    if len(r1.boxes) > len(r2.boxes):
        result = img1
    else:
        result = img2

    cv2.imshow("Fusion YOLO", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()