from imutils import resize
import numpy as np
import cv2
import base64

from classes import KTPData

def image_to_base64(img):
  return base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()

def image_to_cv2(img):
  cv2_img = np.asarray(bytearray(img.file.read()), dtype="uint8")
  cv2_img = cv2.imdecode(cv2_img, cv2.IMREAD_COLOR)
  return cv2_img

def resize_img(img, width):
  return resize(img,width=width)


def set_ktp_data_custom(data,ktp_img,face_img):
  nik = '-' if len(data) <= 2 else data[2] 
  name = '-' if len(data) <= 3 else data[3] 
  birth_place = '-'
  birth_date = '-' if len(data) <= 4 else data[4] 
  gender = '-' if len(data) <= 5 else data[5] 
  blood_type = '-' if len(data) <= 6 else data[6] 
  street_address = '-' if len(data) <= 7 else data[7] 
  rt_number = '-' if len(data) <= 8 else data[8] 
  rw_number = '-' if len(data) <= 8 else data[8] 
  village = '-' if len(data) <= 9 else data[9] 
  sub_district = '-' if len(data) <= 10 else data[10] 
  district = '-' if len(data) <= 1 else data[1] 
  religion = '-' if len(data) <= 11 else data[11] 
  marital_status = '-' if len(data) <= 12 else data[12] 
  job = '-' if len(data) <= 13 else data[13] 
  nationality = '-' if len(data) <= 14 else data[14] 
  validUntil = '-' if len(data) <= 15 else data[15] 

  ktp_data:KTPData = KTPData(nik=nik,name=name, birthPlace=birth_place,
    birthDate=birth_date,
    gender=gender,
    bloodType=blood_type,
    streetAddress=street_address,
    rtNumber=rt_number,
    rwNumber=rw_number,
    village=village,
    subDistrict=sub_district,
    district=district,
    religion=religion,
    maritalStatus=marital_status,
    job=job,
    nationality=nationality,
    validUntil=validUntil,
    ktp_img=image_to_base64(ktp_img),
    face_img=image_to_base64(face_img))

  return ktp_data


def set_ktp_data_tesseract(data,ktp_img,face_img):
  nik = '-' if len(data) <= 2 else data[2] 
  name = '-' if len(data) <= 3 else data[3] 
  birth_place = '-' if len(data) <= 4 else data[4]
  birth_date = '-' if len(data) <= 5 else data[5] 
  gender = '-' if len(data) <= 6 else data[6] 
  blood_type = '-' if len(data) <= 7 else data[7] 
  street_address = '-' if len(data) <= 8 else data[8] 
  rt_number = '-' if len(data) <= 9 else data[9] 
  rw_number = '-' if len(data) <= 9 else data[9] 
  village = '-' if len(data) <= 10 else data[10] 
  sub_district = '-' if len(data) <= 11 else data[11] 
  district = '-' if len(data) <= 1 else data[1] 
  religion = '-' if len(data) <= 12 else data[12] 
  marital_status = '-' if len(data) <= 13 else data[13] 
  job = '-' if len(data) <= 14 else data[14] 
  nationality = '-' if len(data) <= 15 else data[15] 
  validUntil = '-' if len(data) <= 16 else data[16] 

  ktp_data:KTPData = KTPData(nik=nik,name=name, birthPlace=birth_place,
    birthDate=birth_date,
    gender=gender,
    bloodType=blood_type,
    streetAddress=street_address,
    rtNumber=rt_number,
    rwNumber=rw_number,
    village=village,
    subDistrict=sub_district,
    district=district,
    religion=religion,
    maritalStatus=marital_status,
    job=job,
    nationality=nationality,
    validUntil=validUntil,
    ktp_img=image_to_base64(ktp_img),
    face_img=image_to_base64(face_img))

  return ktp_data