from dependency_injector import containers, providers

from src import Environment
from src.services import ImageProcessor, Processor
from src.detectors import ( 
    YoloDetector,
    CascadeClassifierDetector
)


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    environment = providers.ThreadSafeSingleton(Environment)

    image_processor = providers.ThreadSafeSingleton(
        ImageProcessor
    )

    if environment().detector_used == "YOLOV8":
        detector = providers.ThreadSafeSingleton(YoloDetector)
    elif environment().detector_used == "CASCADE_CLASSIFIER":
        detector = providers.ThreadSafeSingleton(CascadeClassifierDetector)
    else:
        raise ValueError("Undefined option for detector selection")

    processor = providers.ThreadSafeSingleton(
        Processor, 
        image_processor=image_processor,
        detector=detector,
    )