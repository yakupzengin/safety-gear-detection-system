from ultralytics import YOLO
import cv2

class YOLOModel:
    def __init__(self,model_path):
        self.model = YOLO(model_path)

    def predict(self,frame):
        return self.model.predict(frame)