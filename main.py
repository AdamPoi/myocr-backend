from fastapi import FastAPI, File, UploadFile,Path,Response,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from pydantic_settings import BaseSettings
import io
import os
import cv2
import uuid


from classes import KTPData,FuzzyData
from preprocessing import grab_ktp_data,filter_image,extract_face
from localization import localize_ktp
from recognition import custom_recognize_ktp,tesseract_recognize_ktp
from helper import set_ktp_data_custom,set_ktp_data_tesseract,resize_img,image_to_cv2,image_to_base64
from fuzzy_tsukamoto import TsukamotoFuzzyLogic

class Settings():

    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"

class KTPImg():
  ktp_image:str

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
      # try:
      localized_ktp = localize_ktp(ori_img)
      resized_img = resize_img(localized_ktp,2560)
      ktp_img,face_img,ktp_roi = grab_ktp_data(resized_img)

      data = custom_recognize_ktp(ktp_roi)
      print(data)
      ktp_data = set_ktp_data_custom(data,ktp_img,face_img)
      
      return {'data':ktp_data}
      # except Exception as error:
      #   raise HTTPException(status_code=403, detail=f"KTP Tidak Terdeteksi{error}")

@app.post("/recognize/ktp/tesseract" )
def recognize_ktp_tesseract(ktp_image: UploadFile = File(...)):
    if not ktp_image:
      raise HTTPException(status_code=422, detail="No upload file sent")
    else:
      # try: 
      ori_img = image_to_cv2(ktp_image)
      localized_ktp = localize_ktp(ori_img)
      resized_img = resize_img(localized_ktp,2560)

      filtered_img = filter_image(resized_img)

      face_img,extracted_img = extract_face(resized_img,filtered_img)

      ktp_data = tesseract_recognize_ktp(extracted_img)

      ktp_data = set_ktp_data_tesseract(ktp_data,resized_img,face_img)
      return {'data':ktp_data}
      # except Exception as error:
      #   raise HTTPException(status_code=403, detail="KTP Tidak Terdeteksi{error}")

@app.post("/ktp/image")
def get_ktp_image(ktp_image: UploadFile = File(...)):
    if not ktp_image:
      raise HTTPException(status_code=422, detail="No upload file sent")
    else:
      ori_img = image_to_cv2(ktp_image)
      localized_ktp = localize_ktp(ori_img)
      resized_img = resize_img(localized_ktp,1280)
      # KTP_img:KTPImg = KTPImg(ktp_image=)

      return {'data':{
        'ktp_image':image_to_base64(resized_img)
        }}



@app.get("/fuzzy")
def calculate_suitability(fuzzy_data: list[FuzzyData]):
    # Calculate suitability using the TsukamotoFuzzyLogic class
    tsukamoto = TsukamotoFuzzyLogic()
    results = []

    for data in fuzzy_data:
      result,rule1,rule2,rule3,rule4,rule5,rule6 = ((tsukamoto.apply_rules(data)))
      results.append({"id":data.id,"name":data.name,"score":result,
        "location":rule1,
        "age":rule2,
        "experience":rule3,
        "skill":rule4,
        "ipk":rule5,
        "org_exp":rule6
      })

    # Sort the results in descending order
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    return {"data": sorted_results}

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5001))
	run(app, host="127.0.0.1", port=port)