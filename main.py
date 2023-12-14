from fastapi import FastAPI, File, UploadFile,Path,Response,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from pydantic_settings import BaseSettings
import io
import os
import cv2
import uuid


from classes import KTPData
from preprocessing import grab_ktp_data,filter_image,extract_face
from localization import localize_ktp
from recognition import custom_recognize_ktp,tesseract_recognize_ktp
from helper import set_ktp_data_custom,set_ktp_data_tesseract,resize_img,image_to_cv2

class Settings():

    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"


settings = Settings()

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

if settings.USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8000"

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.BASE_URL = public_url
    init_webhooks(public_url)

KTP_PATH = "images/ktp"

@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to the API home page!"}

@app.post("/recognize/ktp/custom")
def recognize_ktp_custom(ktp_image: UploadFile = File(...)):
    if not ktp_image:
      raise HTTPException(status_code=422, detail="No upload file sent")
    else:
      ori_img = image_to_cv2(ktp_image)

      (_,_,_,localized_ktp) = localize_ktp(ori_img)
      resized_img = resize_img(localized_ktp,1280)
      ktp_img,face_img,ktp_roi = grab_ktp_data(resized_img)
      ktp_data = custom_recognize_ktp(ktp_roi)

      ktp_data = set_ktp_data_custom(ktp_data,ktp_img,face_img)
      
      return {'data':ktp_data}

@app.post("/recognize/ktp/tesseract" )
def recognize_ktp_tesseract(ktp_image: UploadFile = File(...)):
    if not ktp_image:
      raise HTTPException(status_code=422, detail="No upload file sent")
    else:
      ori_img = image_to_cv2(ktp_image)
      (_,_,_,localized_ktp) = localize_ktp(ori_img)
      resized_img = resize_img(localized_ktp,1280)
      filtered_img = filter_image(resized_img)
      cv2.imwrite(f'ktp/img/{uuid.uuid1()}.jpg',filtered_img)

      face_img,extracted_img = extract_face(resized_img,filtered_img)
      # ktp_img,face_img,ktp_roi = grab_ktp_data(ktp_image)
      ktp_data = tesseract_recognize_ktp(extracted_img)

      ktp_data = set_ktp_data_tesseract(ktp_data,resized_img,face_img)
      
      return {'data':ktp_data}


    

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5001))
	run(app, host="127.0.0.1", port=port)