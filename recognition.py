from fastapi import BackgroundTasks
from tensorflow.keras.models import load_model
from imutils import contours,grab_contours
import cv2
import numpy as np
import pytesseract



MODEL_PATH = "models/custom_ocr_6_lstm_bs128_40ep_66_model.h5"
# MODEL_PATH = "models/custom_ocr_4_20ep_94_model"

# CLASS_MAPPING = [
#     '!', '"', '#', '$', '%', '&', "'", '(', ')', '*',
#     '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
#     '5', '6', '7', '8', '9', ':', ';', '<', '=', '>',
#     '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
#     'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
#     'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'W', 'X',
#     'Y', 'Z', '!', '"', 'a', 'b', 'c', 'd', "e", 'f',
#     'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
#     'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
#     '{', '|', '}', '~']

CLASS_MAPPING =['6', 'D', 'f', '/', 'F', 'x', 'J', '8', 'H', 'k',  
                '1', 'g', '2', 'd', '3', 't', '.', '4', 'o', 'y', 
                'A', 'u', 'G', '-', 'm', 'W', 'c', '9', 'N', 'P', 
                'X', 'h', '7', 'j', '5', 'b', 'w', 'l', '0', 'I', 
                'Y', ':', 'T', 'K', 'E', 'V', 'M', 'S', 'a', 'i', 
                'r', 'p', 'e', 'U', 's', 'C', 'q', 'n', 'B', 'z', 
                'v', 'O', 'R', 'Z', 'Q', 'L']

model = load_model(MODEL_PATH)

def custom_recognize_ktp(ktp_roi):
  recognition_results = []
  for i,roi in enumerate(ktp_roi):
    # split gender and blood type
    if(i == 5):
      text_roi = grab_text(roi,1)
      pred = recognize_text(text_roi)
      recognition_results.append(pred)

    text_roi = grab_text(roi,-1)
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
    if(w > 4 and h > 20):
      padded = cv2.copyMakeBorder(text_roi[y:y+h, x:x+w],16,16,16,16, cv2.BORDER_CONSTANT)
      # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,5))
      # dilate = cv2.morphologyEx(ktp_img, cv2.MORPH_DILATE, kernel, iterations=1)
      padded = cv2.resize(padded,(28,28))
      pad = np.array(padded)
      pad_vector = pad.reshape((-1, 1))
      padded = pad_vector.reshape(-1, 28, 28, 1)

      pred = model.predict(padded)
      pred_index = np.argmax(pred)
      text.append(f'{CLASS_MAPPING[pred_index]}')
  return ''.join(text)

def grab_text(ktp_roi,index):
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,40))
  dlt = cv2.dilate(ktp_roi, rect_kernel, iterations = 1)

  cnts = cv2.findContours(dlt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = grab_contours(cnts)
  cnts = contours.sort_contours(cnts, method="left-to-right")[0]
  x, y, w, h = cv2.boundingRect(cnts[index])

  return ktp_roi[y:y+h, x:x+w]



def tesseract_recognize_ktp(ktp_img):
  recognition_results = []
  # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,5))
  # dilate = cv2.morphologyEx(ktp_img, cv2.MORPH_DILATE, kernel, iterations=1)
  pred = pytesseract.image_to_string(ktp_img,lang='ind',config='--psm 6')
  for word in pred.split("\n"):
    if word == "": continue
    if "”—" in word:
      word = word.replace("”—", ":")
    #normalize NIK
    if "NIK" in word:
      nik_char = word.split()
      if "D" in word:
        word = word.replace("D", "0")
      if "?" in word:
        word = word.replace("?", "7")
    recognition_results.append(word)
  return recognition_results


def normalize_text(text):
  if "“" in text:
      text = text.replace("“", "")
  if ":" in text:
      text = text.replace(":", "")
      
  if text.find("\n") != -1:
      text = text.replace("\n", "")
  text = text.strip()
  return text
