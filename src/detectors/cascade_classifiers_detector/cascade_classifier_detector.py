import cv2
import numpy as np
from PIL import Image
from PIL.ImageFile import ImageFile

from src.interfaces import AbstractVehicleDetector

from src.models import DetectionRequestDto, DetectionResultDto


class CascadeClassifierDetector(AbstractVehicleDetector):
    '''
    This detector is implemented using the Cascade Classifiers based on instructions
    found on https://medium.com/@kaanerdenn/introduction-to-object-detection-vehicle-detection-with-opencv-and-cascade-classifiers-8c6834191a0b
    '''
    CLASSIFIER_FILE_PATH = (
        "/home/eonrrfe/Documents/Repos/Others/CarDetection/src/computer_vision"
        "/detectors/cascade_classifiers_detector/cars.xml"
    )

    def __init__(self):
        self._cascade_classifier = self._load_cascade_classifier()

    def _resize(self, image: ImageFile) -> Image:
        image_copy = image.copy()
        return image_copy.resize((768, 1024)) 

    def _load_cascade_classifier(self) -> cv2.CascadeClassifier:
        return cv2.CascadeClassifier(self.CLASSIFIER_FILE_PATH)

    def _convert_to_greyscale(self, image_array: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    
    def _apply_gaussian_blur(self, image_array: np.ndarray) -> np.ndarray:
        return cv2.GaussianBlur(image_array, (5, 5), 0)
    
    def _dilate_image(self, image_array: np.ndarray) -> np.ndarray:
        return cv2.dilate(image_array, np.ones((3, 3)))
    
    def _apply_morph_closing(self, image_array: np.ndarray) -> np.ndarray:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        return cv2.morphologyEx(image_array, cv2.MORPH_CLOSE, kernel)
    
    def detect_and_count(
        self, detection_request: DetectionRequestDto
    ) -> DetectionResultDto:
        # resize image because the classifier is trained to work
        # with smaller reoslution images - scaling factor is 2
        resized_image = self._resize(detection_request.image)

        image_array = np.asarray(resized_image)

        # Convert the image to grayscale - color is not important information with this detection method
        # so we remove it to reduce memory usage, noise and computational complexity.
        grey_image = self._convert_to_greyscale(image_array)

        # Apply Gaussian blur to the grayscale image - Gaussian blur smooths the image 
        # by averaging pixel values in a neighborhood. It’s beneficial for reducing noise, 
        # enhancing features, and preparing the image for more accurate analysis in tasks 
        # like edge detection and object recognition.
        blur_image = self._apply_gaussian_blur(grey_image)

        # Apply dilation to the blurred image - Dilation expands bright regions in the image, helping to 
        # enhance object boundaries and remove small noise. It’s a common step in image 
        # preprocessing for tasks like object detection and segmentation.
        dilated_image = self._dilate_image(blur_image)

        # Apply morphological closing to the dilated image
        closing_image = self._apply_morph_closing(dilated_image)

        detections = self._cascade_classifier.detectMultiScale(
            closing_image, 1.5, 1
        )

        # count and annotate cars on the image
        boundary_boxes = []
        orig_image_array = np.array(detection_request.image)
        for (x, y, w, h) in detections:
            # scale to original image size
            x_i = 2*x
            y_i = 2*y
            w_i = 2*w
            h_i = 2*h
            if (
                detection_request.process_request.parameters.
                include_boundary_boxes
            ):
                cv2.rectangle(
                    orig_image_array, 
                    (x_i, y_i), 
                    (x_i + w_i, y_i + h_i), 
                    (255, 0, 0), 
                    2
                )
            # append each boundary box: 
            boundary_boxes.append(
                [
                    [x_i, y_i], 
                    [x_i+w_i, y_i+h_i], 
                ]
            )

        return DetectionResultDto(
            detection_request=detection_request,
            inferred_image=Image.fromarray(orig_image_array),
            boundary_boxes=np.array(boundary_boxes),
            count=len(boundary_boxes)
        )
