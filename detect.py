#import numpy as np
import cv2
import os

print("Path at terminal when executing this file")
print(os.getcwd())

# Load our cascade classifier from cars3.xml
car_cascade = cv2.CascadeClassifier(r'classifier/banana_classifier.xml')

image = cv2.imread('images/image1.jpg')

# Crop so that only the roads remain, eliminatives the distraction.
#image = image[120:,:-20]

# Use Cascade Classifier to detect cars, may have to tune the
# parameters for less false positives.
cars = car_cascade.detectMultiScale(image, 1.1, 2)
for (x,y,w,h) in cars:
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

print('Processing', 1, ' : bananas detected : ', len(cars))

cv2.imwrite('images/'+ 'processed.jpg', image)

