from imutils import contours,grab_contours
import numpy as np
import cv2

from helper import resize_img

ktp_roi = []
ori_img = []

def grab_ktp_data(ktp_image):
  filtered_img = filter_image(ktp_image)
  face_img,extracted_img = extract_face(ktp_image,filtered_img)

  grab_contour(extracted_img)
  
  return [ktp_image,face_img,ktp_roi]


def filter_image(image):
  gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
  blurred = cv2.GaussianBlur(gray,(5,5),0)
  thresholded = cv2.threshold(blurred,165,255,cv2.THRESH_TRUNC + cv2.THRESH_OTSU)[1]
  binary = cv2.threshold(thresholded,127,255,cv2.THRESH_BINARY_INV)[1]
  # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
  # dilation = cv2.erode(binary, rect_kernel, iterations = 1)
  
  return binary


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


