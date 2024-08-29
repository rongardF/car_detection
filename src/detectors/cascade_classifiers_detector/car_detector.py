# project is created based on tutorial: 
# https://medium.com/@kaanerdenn/introduction-to-object-detection-vehicle-detection-with-opencv-and-cascade-classifiers-8c6834191a0b

#TODO:
# 1. Think how to corretcly resize fullHD (2048x1536) to expected size of 931x524 with correct resolution - depend on camera probably
# 2. Think about the whole process from API point of view:
#   - what needs to be input (image, usable area from the camera, direction of cars counting etc., camera parameters)
#   - what will be the output from the API call?
# 3. Think about more advanced CV methods to detect cars, busses and motorcycles
#   - https://patricia-schutter.medium.com/car-image-recognition-with-convolutional-neural-network-applications-e791c98c9d72
# 4. Find a suitable IP camera:
#   - battery powered (possibly sun panel re-charged)
#   - can stream images over mobile network to cloud
#   - can be configured to sleep-wakeup-picture-send-sleep routine

from PIL import Image
import cv2
import numpy as np
import requests
import sys

SHOW_IMAGES_LEVELED_FLAGS = {0: False, 1: False, 2: False, 3: False, 4: False, 5: True}
DOWNLOAD = False
PROCESS_IMAGE = True

# get image
if DOWNLOAD:
    IMAGE_URL = 'https://a57.foxnews.com/media.foxbusiness.com/BrightCove/854081161001/201805/2879/931/524/854081161001_5782482890001_5782477388001-vs.jpg'
    response = requests.get(IMAGE_URL, stream=True)
    image_original = Image.open(response.raw)
else:
    IMAGE_PATH = "/home/eonrrfe/Documents/Repos/Others/CarDetection/test_images/cars_1.JPEG"
    image = Image.open(IMAGE_PATH)
    # image_original_resized = image.resize((931, 699))
    # image_original_resized.show()
    # sys.exit()
    left = 500
    top = 200
    image_original = image.crop((left, top, left+1131, top+879 ))
    # image_original.show()
    # sys.exit()

# resizing the image 
if SHOW_IMAGES_LEVELED_FLAGS[0]:
    image_original.show()
image_resized = image_original.resize((450, 250))  # affects the quality and resolution of pictures
if SHOW_IMAGES_LEVELED_FLAGS[0]:
    image_resized.show()

if PROCESS_IMAGE:
    # Convert the image to a Numpy array
    image_arr = np.array(image_resized)

    # Convert the image to grayscale - color is not important information with this detection method
    # so we remove it to reduce memory usage, noise and computational complexity.
    grey_image = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
    if SHOW_IMAGES_LEVELED_FLAGS[1]:
        cv2.imshow("Grayscale Image", grey_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Apply Gaussian blur to the grayscale image - Gaussian blur smooths the image 
    # by averaging pixel values in a neighborhood. It’s beneficial for reducing noise, 
    # enhancing features, and preparing the image for more accurate analysis in tasks 
    # like edge detection and object recognition.
    blur_image = cv2.GaussianBlur(grey_image, (5, 5), 0)
    if SHOW_IMAGES_LEVELED_FLAGS[2]:
        cv2.imshow("Blurred Image", blur_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # Apply dilation to the blurred image - Dilation expands bright regions in the image, helping to 
    # enhance object boundaries and remove small noise. It’s a common step in image 
    # preprocessing for tasks like object detection and segmentation.
    dilated_image = cv2.dilate(blur_image, np.ones((3, 3)))
    if SHOW_IMAGES_LEVELED_FLAGS[3]:
        cv2.imshow("Dilated Image", dilated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # Apply morphological closing to the dilated image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    closing_image = cv2.morphologyEx(dilated_image, cv2.MORPH_CLOSE, kernel)
    if SHOW_IMAGES_LEVELED_FLAGS[4]:
        cv2.imshow("Morphologically Closed Image", closing_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # Use CascadeClassifier for car detection
    car_cascade_src = 'cars.xml'
    car_cascade = cv2.CascadeClassifier(car_cascade_src)
    cars = car_cascade.detectMultiScale(closing_image, 1.5, 1)

    # count and annotate cars on the image
    cnt = 0
    for (x, y, w, h) in cars:
        cv2.rectangle(image_arr, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cnt += 1

    # Convert the annotated image to PIL Image format and display it
    if SHOW_IMAGES_LEVELED_FLAGS[5]:
        annotated_image = Image.fromarray(image_arr)
        annotated_image.show()

    # Close the window when a key is pressed
    cv2.waitKey(0)
    cv2.destroyAllWindows()