from fastapi import FastAPI, File, UploadFile,Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from uvicorn import run
import uuid
import io
import os
import cv2


from classes import KTPImg
from preprocessing import grab_ktp_data
from recognition import recognize_ktp
from helper import set_ktp_data



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
      ori_img,face_img,ktp_roi = grab_ktp_data(ktp_img)
      ktp_data = recognize_ktp(ktp_roi)
      print(len(ktp_data))
      ktp_data = set_ktp_data(ktp_data)
      
      return {"ktp_img": ori_img,'face_img':face_img,'data':ktp_data}
    

@app.get("/ktp/image")
async def get_ktp_image(ktp_img:KTPImg):

    file_location = f"{KTP_PATH}/{ktp_img.filename}"
    
    return {"name": ktp_img.filename,"image":FileResponse(path=file_location)}


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5001))
	run(app, host="127.0.0.1", port=port)