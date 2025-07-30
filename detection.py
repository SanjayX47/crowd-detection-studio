import cv2
from ultralytics import YOLO
import numpy as np

class CrowdDetector:
    def __init__(self, update_callback=None):
        self.model = YOLO("yolov8n.pt")  # Pretrained on COCO
        self.update_callback = update_callback

    def detect_webcam(self, stop_condition):
        cap = cv2.VideoCapture(0)
        heatmap_acc = np.zeros((480, 640), dtype=np.float32)

        while True:
            if stop_condition():
                break
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model(frame)
            annotated = results[0].plot()

            person_boxes = [box for box in results[0].boxes if int(box.cls) == 0]  # Keep only person class

            for box in person_boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                heatmap_acc[y1:y2, x1:x2] += 1

            heatmap_color = cv2.applyColorMap(
                cv2.normalize(heatmap_acc, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8),
                cv2.COLORMAP_JET
            )

            count = len(person_boxes)
            if self.update_callback:
                self.update_callback(annotated, heatmap_color, count)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()

    def detect_video(self, path, stop_condition):
        cap = cv2.VideoCapture(path)
        heatmap_acc = np.zeros((480, 640), dtype=np.float32)

        while True:
            if stop_condition():
                break
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model(frame)
            annotated = results[0].plot()

            person_boxes = [box for box in results[0].boxes if int(box.cls) == 0]  # Only person

            for box in person_boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                heatmap_acc[y1:y2, x1:x2] += 1

            heatmap_color = cv2.applyColorMap(
                cv2.normalize(heatmap_acc, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8),
                cv2.COLORMAP_JET
            )

            count = len(person_boxes)
            if self.update_callback:
                self.update_callback(annotated, heatmap_color, count)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
