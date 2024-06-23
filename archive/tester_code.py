import cv2
import numpy as np

# Load pre-trained model (for example, using a deep learning model like MobileNet)
model = cv2.dnn.readNet('model.caffemodel', 'model.prototxt')

def identify_medicine(image_path):
    image = cv2.imread(image_path)
    blob = cv2.dnn.blobFromImage(image, 1.0, (224, 224), (104, 117, 123))
    model.setInput(blob)
    output = model.forward()
    # Process the output to get the medicine type
    medicine_type = np.argmax(output)
    return medicine_type

# Example usage
medicine_type = identify_medicine(r'C:\Users\Gaurav\PharmaSee\Images\Acretin 30 g cream\huawei cn (48).jpg')
print(f'Medicine type: {medicine_type}')