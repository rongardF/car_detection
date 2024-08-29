from typing import List
import pathlib
import cv2
import numpy as np
import math
from PIL import Image
from PIL.ImageFile import ImageFile

from ultralytics import YOLO 
from ultralytics.engine.results import Boxes

from src.interfaces import AbstractVehicleDetector

from src.models import DetectionDto


class YoloDetector(AbstractVehicleDetector):
    '''
    This detector is implemented using the YOLOv8 based on instructions
    found on https://medium.com/@martin.jurado.p/my-first-ai-project-with-yolo-real-time-object-detection-bc8669c583ab
    '''
    CLASS_NAMES = [
        "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
        "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
        "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
        "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
        "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
        "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
        "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
        "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
        "teddy bear", "hair drier", "toothbrush"
    ]

    # indexes of the classes from above list which we try to detect
    VECHICLE_INDEXES = [2, 3, 5, 7]

    # pre-trained model by 'ultralytics'
    PATH_TO_MODEL = (
        f"{pathlib.Path(__file__).parent.resolve()}/yolo-Weights/yolov8n.pt"
    )

    def __init__(self):
        self._model = YOLO(self.PATH_TO_MODEL)  # Load YOLOv8 model with pre-trained weights
    
    def _extract_boundary_boxes(self, boxes: List[Boxes]) -> np.ndarray:
        boundary_boxes = []

        for box in boxes:
            if int(box.cls[0]) not in self.VECHICLE_INDEXES:
                continue  # only detect motor-vechicles on the image

            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to integer values

            boundary_boxes.append(
                [
                    [x1, y1], 
                    [x2, y2], 
                ]
            )

        return np.array(boundary_boxes)

    def _apply_overlay(self, boxes: List[Boxes], image_array: np.ndarray) -> np.ndarray:
        # Iterate through each bounding box
        for box in boxes:
            if int(box.cls[0]) not in self.VECHICLE_INDEXES:
                continue  # only detect motor-vechicles on the image

            # Extract coordinates of the bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to integer values

            # Draw the bounding box on the frame
            cv2.rectangle(
                img=image_array, 
                pt1=(x1, y1), 
                pt2=(x2, y2), 
                color=(255, 0, 255), 
                thickness=3
            )

            # Overlay class name and confidence
            confidence = math.ceil((box.conf[0]*100))/100
            cls = int(box.cls[0])
            text = f"{self.CLASS_NAMES[cls]}:{confidence}"

            cv2.putText(
                img=image_array, 
                text=text, 
                org=[x1, y1], 
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=1, 
                color=(255, 0, 0), 
                thickness=2
            )
        
        return image_array
    
    def detect_and_count(self, image: ImageFile) -> DetectionDto:
        # copy and convert to numpy array
        image_array = np.array(image)

        # infer objects from the image
        result = self._model(image_array, stream=False)[0]

        inferred_image = self._apply_overlay(result.boxes, image_array)

        boundary_boxes = self._extract_boundary_boxes(result.boxes)

        return DetectionDto(
            inferred_image=Image.fromarray(inferred_image),
            boundary_boxes=boundary_boxes,
            count=len(boundary_boxes)
        )
