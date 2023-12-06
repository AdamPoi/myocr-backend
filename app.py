from fastapi import FastAPI, File, UploadFile,Path
from fastapi.responses import FileResponse
import uuid
import io
from cv2 import imwrite

import preprocessing

from models import KTPImg,KTPData

app = FastAPI()

KTP_PATH = "images/ktp"
KTP_DATA:KTPData = KTPData

@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to the API home page!"}

@app.post("/ktp/image")
async def upload_ktp_image(ktp_img: UploadFile = File(...)):
    if not ktp_img:
      return {"message": "No upload file sent"}
    else:
      file_name = f"ktp-{uuid.uuid1()}.{ktp_img.filename.split('.')[-1]}"
      file_location = f"{KTP_PATH}/{file_name}"

      with open(file_location, "wb+") as file_object:
        foto_wajah,ktp_roi = preprocessing.preprocessing_image(ktp_img)
        KTP_DATA.cardPhotoUrl=foto_wajah
        for i,p in enumerate(ktp_roi):
          imwrite(f"{f"{KTP_PATH}/{i}-{file_name}"}",p)

        return {"info": f"file '{file_name}' saved at '{KTP_DATA.cardPhotoUrl}'"}
    

@app.get("/ktp/image")
async def get_ktp_image(ktp_img:KTPImg):

    file_location = f"{KTP_PATH}/{ktp_img.filename}"
    
    return {"name": ktp_img.filename,"image":FileResponse(path=file_location)}