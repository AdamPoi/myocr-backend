import numpy as np
import imutils
import cv2
from imutils import contours

ktp_roi = []
ori_img = []

def preprocessing_image(ktp_image):
  ori_img = read_cv2_image(ktp_image)
  filtered_img = filter_image(ori_img)
  foto_wajah,removed_foto = remove_foto_ktp(ori_img,filtered_img)
  get_ktp_contour(removed_foto)

  return [foto_wajah,ktp_roi]

def filter_image(image):
  gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
  thresholded = cv2.threshold(gray,127,255,cv2.THRESH_TRUNC + cv2.THRESH_OTSU)[1]

  # kernel = np.array([[-2,0,-2],[0,10,0],[-2,0,-2]])
  # sharpened = cv2.filter2D(thresholded,-1,kernel)
  # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
  # opened = cv2.morphologyEx(sharpened,cv2.MORPH_OPEN, kernel, iterations=1)
  # dilated = cv2.erode(sharpened,kernel)
  # blurred = cv2.GaussianBlur(thresholded,(3,3),0)
  # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(12, 12))
  # clahed = clahe.apply(blurred)
  binary = cv2.threshold(thresholded,127,255,cv2.THRESH_BINARY_INV)[1]
  # canny = cv2.Canny(opened,100,200)
  return binary


def read_cv2_image(ktp_image):
    image = np.asarray(bytearray(ktp_image.file.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def remove_foto_ktp(ori_img,filtered_img):
  #cari kontur
  cnts = cv2.findContours(filtered_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = imutils.grab_contours(cnts)
  cnts = contours.sort_contours(cnts, method="left-to-right")[0]

  # crop foto wajah ktp
  largest_areas = sorted(cnts, key=cv2.contourArea)
  x, y, w, h = cv2.boundingRect(largest_areas[-1])
  cv2.rectangle(filtered_img, (x, y), (x + w, y + h), (0, 0, 0), -1)

  foto_ktp = ori_img[y:y+h, x:x+w]
  return [foto_ktp,filtered_img]

def get_ktp_contour(filtered_image):
  # dilatasi kotak
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (120,1))
  dilation = cv2.dilate(filtered_image, rect_kernel, iterations = 1)

  # cari kontur teks
  cnts = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cnts = imutils.grab_contours(cnts)
  cnts = contours.sort_contours(cnts, method="top-to-bottom")[0]
  
  # gambar kotak pada kontur teks
  for cnt in cnts:
    get_ktp_roi(cnt,filtered_image)

def get_ktp_roi(cnt,filtered_image):
  x, y, w, h = cv2.boundingRect(cnt)
  if(w > 8 and h > 10):
    roi = filtered_image[y:y+h, x:x+w]
    padded_roi = cv2.copyMakeBorder(roi, 8, 8, 8, 8, cv2.BORDER_CONSTANT)
    padded_roi = 255 - padded_roi
    ktp_roi.append(padded_roi)
  else:
    return 

