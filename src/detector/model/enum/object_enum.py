from enum import Enum


class ObjectEnum(Enum):
    # NOTE: enum values must be kept in sync with values used in model(s)
    
    VEHICLE = "vehicle"
    CAR = "car"
    MOTORBIKE = "motorbike"
    BICYCLE = "bicycle"
    BUS = "bus"
    TRUCK = "truck"
