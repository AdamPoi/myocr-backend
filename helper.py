import numpy as np
import cv2
from imutils import resize
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


def set_ktp_data(data):
  nik = data[2]
  name = data[3]
  birth_place = '-'
  birth_date = data[4]
  gender = data[5]
  blood_type = data[6]
  street_address = data[7]
  rt_number = data[8]
  rw_number = data[8]
  # # kelurahan/desa
  village = data[9]
  # # kecamatan
  sub_district = data[10]
  # # kabupaten/kota
  district = data[1]
  religion = data[11]
  marital_status = data[12]
  job = data[13]
  nationality = data[14]
  validUntil = data[15]

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
    validUntil=validUntil)

  return ktp_data