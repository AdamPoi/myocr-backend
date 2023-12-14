from tensorflow.keras.models import load_model
from imutils import contours,grab_contours
import cv2
import numpy as np
import pytesseract


MODEL_PATH = "models/custom_ocr_4_20ep_94_model"

CLASS_MAPPING = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*',
    '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', ':', ';', '<', '=', '>',
    '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'W', 'X',
    'Y', 'Z', '!', '"', 'a', 'b', 'c', 'd', "e", 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '{', '|', '}', '~']

model = load_model(MODEL_PATH)
recognition_results = []

def custom_recognize_ktp(ktp_roi):
  for i,roi in enumerate(ktp_roi):
    padded = cv2.copyMakeBorder(roi, 12, 12, 12, 12, cv2.BORDER_CONSTANT)

    # split gender and blood type
    if(i == 5):
      text_roi = grab_text(padded,1)
      pred = recognize_text(text_roi)
      recognition_results.append(pred)

    text_roi = grab_text(padded,-1)
    pred = recognize_text(text_roi)
    recognition_results.append(pred)
  return recognition_results

def recognize_text(text_roi):
  text=[]
  cnts = cv2.findContours(text_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = grab_contours(cnts)
  cnts = contours.sort_contours(cnts, method="left-to-right")[0]

  for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if(w > 14 and h > 14):
          padded = cv2.copyMakeBorder(text_roi[y:y+h, x:x+w],6,6,6,6, cv2.BORDER_CONSTANT)
          padded = cv2.resize(padded,(28,28))

          pad = np.array(padded)
          pad = pad / 255.0
          pad_vector = pad.reshape((-1, 1))
          padded = pad_vector.reshape(-1, 28, 28, 1)

          pred = model.predict(padded)
          pred_index = np.argmax(pred)
          text.append(f'{CLASS_MAPPING[pred_index]}')
  return ''.join(text)

def grab_text(ktp_roi,index):
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20,20))
  dlt = cv2.dilate(ktp_roi, rect_kernel, iterations = 1)

  cnts = cv2.findContours(dlt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = grab_contours(cnts)
  cnts = contours.sort_contours(cnts, method="left-to-right")[0]
  x, y, w, h = cv2.boundingRect(cnts[index])

  return ktp_roi[y:y+h, x:x+w]

def tesseract_recognize_ktp(ktp_img):
  pred = pytesseract.image_to_string(ktp_img,lang='ind',config='--psm 6')
  for word in pred.split("\n"):
    if "”—" in word:
      word = word.replace("”—", ":")
    #normalize NIK
    if "NIK" in word:
      nik_char = word.split()
      if "D" in word:
        word = word.replace("D", "0")
      if "?" in word:
        word = word.replace("?", "7")
    if ":" in word:
      word = word.split(":")[1] 
    # word = normalize_text(word)
    recognition_results.append(word)
  return recognition_results

# def tesseract_recognize_ktp(ktp_roi):
#   for i,roi in enumerate(ktp_roi):
#     padded = cv2.copyMakeBorder(roi, 12, 12, 12, 12, cv2.BORDER_CONSTANT)

#     #split gender and blood type
#     if(i == 5):
#       text_roi = grab_text(padded,1)
#       pred = pytesseract.image_to_string(text_roi,lang='ind',config='--psm 6')
#       recognition_results.append(normalize_text(pred))

#     text_roi = grab_text(padded,-1)
#     pred = pytesseract.image_to_string(text_roi,lang='ind',config='--psm 6')

#     # normalize NIK
#     if(i == 2):
#         if "D" in pred:
#           pred = pred.replace("D", "0")
#         if "?" in pred:
#           pred = pred.replace("?", "7") 
    
#     # split birth date
#     if(i==4):
#       if ',' in pred:
#         birth_place = pred.split(',')[0]
#         birth_date = pred.split(',')[1]
        
#         recognition_results.append(birth_place)
#         recognition_results.append(birth_date.strip())
#         continue

  
    
#     # split marital status
#     if(i==13):
#       if pred.find("KAWIN") != -1:
#         marital_status = pred.split('KAWIN')[1]
#         recognition_results.append(marital_status)
#         continue
#       if pred.find("BELUM") != -1:
#         marital_status = pred.split('BELUM')[1]
#         recognition_results.append(marital_status)
#         continue
#     recognition_results.append(normalize_text(pred))

#   return recognition_results

def normalize_text(text):
  if "“" in text:
      text = text.replace("“", "")
  if ":" in text:
      text = text.replace(":", "")
      
  if text.find("\n") != -1:
      text = text.replace("\n", "")
  text = text.strip()
  return text
