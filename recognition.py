from tensorflow.keras.models import load_model
import imutils
from imutils import contours
import cv2
import numpy as np
import uuid


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

def get_ktp_data(ktp_roi):
  for roi in ktp_roi:
    padded = cv2.copyMakeBorder(roi, 8, 8, 8, 8, cv2.BORDER_CONSTANT)
    cv2.imwrite(f'images/ktp/img-{uuid.uuid1()}.jpg',padded)
    
    # padded = imutils.resize(padded,width=roi.shape[1] * 2)
    pred = get_text_roi(padded)
    print(pred)
    recognition_results.append(pred)
  return recognition_results

def get_text_roi(image):
  text_roi=[]
  cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = imutils.grab_contours(cnts)
  cnts = contours.sort_contours(cnts, method="left-to-right")[0]

  for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if(w > 14 and h > 14):
          padded = cv2.copyMakeBorder(image[y:y+h, x:x+w],12,12,12,12, cv2.BORDER_CONSTANT)

          # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
          # padded = cv2.erode(padded,kernel)
          padded = cv2.resize(padded,(28,28))
          # padded = 255 - padded
          # cv2_imshow(padded)
          pad = np.array(padded)
          pad = pad / 255.0
          pad_vector = pad.reshape((-1, 1))
          padded = pad_vector.reshape(-1, 28, 28, 1)

          pred = model.predict(padded)
          # pred_conf = np.amax(pred)
          pred_index = np.argmax(pred)
          # print(f'model 1 - pred idx: {pred_index}')
          # print(f'model 1 - pred conf: {pred_conf}')
          # print(f'model 1 - pred label: {class_mapping[pred_index]}')
          text_roi.append(f'{CLASS_MAPPING[pred_index]}')
  return ''.join(text_roi)