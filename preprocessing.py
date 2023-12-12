import numpy as np
import cv2

from imutils import contours,grab_contours
from helper import image_to_cv2,resize_img,image_to_base64

ktp_roi = []
ori_img = []

def grab_ktp_data(ktp_image):
  ori_img = image_to_cv2(ktp_image)
  resized_img = resize_img(ori_img,1280)
  filtered_img = filter_image(resized_img)
  face_img,extracted_img = extract_face(ori_img,filtered_img)
  grab_contour(extracted_img)

  return [image_to_base64(ori_img),image_to_base64(face_img),ktp_roi]

def filter_image(image):
  gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
  blurred = cv2.GaussianBlur(gray,(5,5),0)
  thresholded = cv2.threshold(blurred,165,255,cv2.THRESH_TRUNC + cv2.THRESH_OTSU)[1]
  binary = cv2.threshold(thresholded,127,255,cv2.THRESH_BINARY_INV)[1]
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
  dilation = cv2.erode(binary, rect_kernel, iterations = 1)
  return dilation


def extract_face(ori_img,filtered_img):
  #cari kontur
  cnts = cv2.findContours(filtered_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = grab_contours(cnts)
  cnts = contours.sort_contours(cnts, method="left-to-right")[0]

  # crop foto wajah ktp
  largest_areas = sorted(cnts, key=cv2.contourArea)
  x, y, w, h = cv2.boundingRect(largest_areas[-1])
  cv2.rectangle(filtered_img, (x, y), (x + w, y + h), (0, 0, 0), -1)

  face_img = ori_img[y:y+h, x:x+w]

  return [face_img,filtered_img]

def grab_contour(filtered_image):
  # dilatasi kotak
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (240,1))
  dilation = cv2.dilate(filtered_image, rect_kernel, iterations = 1)

  # cari kontur teks
  cnts = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = grab_contours(cnts)
  cnts = contours.sort_contours(cnts, method="top-to-bottom")[0]
  
  # gambar kotak pada kontur teks
  for cnt in cnts:
    grab_ktp_roi(cnt,filtered_image)

def grab_ktp_roi(cnt,filtered_image):
  x, y, w, h = cv2.boundingRect(cnt)
  if(w > 24 and (h > 24 and h < 50)):
    roi = filtered_image[y:y+h, x:x+w]
    padded_roi = cv2.copyMakeBorder(roi, 12, 12, 12, 12, cv2.BORDER_CONSTANT)
    ktp_roi.append(padded_roi)
  else:
    return 

