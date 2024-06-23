import ipdb
import easyocr
import cv2 as cv
import pandas as pd


drug_file = r'C:\Users\Gaurav\PharmaSee\Images\drug list.xlsx'
drugs_list = pd.read_excel(drug_file)
drugs_list, drugs_type = list(drugs_list['Name']), list(drugs_list['Type'])

reader = easyocr.Reader(['en'])
tmp_img_path = r'C:\Users\Gaurav\PharmaSee\Images\img.jpg'

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error. Could not open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error. Could not read frame")
        break
    
    cv.imwrite(tmp_img_path, frame)
    key = cv.waitKey(1)
    case
    result = reader.readtext(tmp_img_path)
    for (_, text, _) in result:
        text = text.lower()
        for i, med in enumerate(drugs_list):
            med = med.lower()
            if (med == text):
                break
    ipdb.set_trace()
    print(f"This medicine is {med[0].upper()}{med[1:]} and it is of type {drugs_type[i]}")