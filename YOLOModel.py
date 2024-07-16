from ultralytics import YOLO
import cv2

class YOLOModel:
    def __init__(self, model_path):
        # Load the YOLO model from the specified path
        self.model = YOLO(model_path)

    def predict(self, frame):
        # Use the model to predict the objects in the given frame
        return self.model.predict(frame)
