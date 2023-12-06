from fastapi import FastAPI, File, UploadFile,Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from uvicorn import run
import uuid
import io
import os


import preprocessing

from models import KTPImg,KTPData


app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers    
)

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

        return {"info": f"file '{file_name}' saved at '{KTP_DATA.cardPhotoUrl}'"}
    

@app.get("/ktp/image")
async def get_ktp_image(ktp_img:KTPImg):

    file_location = f"{KTP_PATH}/{ktp_img.filename}"
    
    return {"name": ktp_img.filename,"image":FileResponse(path=file_location)}


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	run(app, host="127.0.0.1", port=port)