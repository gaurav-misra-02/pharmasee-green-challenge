import easyocr

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify the languages you need

# Load an image and perform OCR
image_path = r'C:\Users\Gaurav\PharmaSee\Images\Aggrex 60 tablets\huawei p30 (559).jpg'
result = reader.readtext(image_path)

print(type(result))

# Print the recognized text
for (bbox, text, prob) in result:
    print(f"Text: {text}, Probability: {prob}")