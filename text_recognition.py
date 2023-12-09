from tensorflow.keras.models import load_model

MODEL_PATH = "models/custom_ocr_4_20ep_94_model"

CLASS_MAPPING = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*',
    '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', ':', ';', '<', '=', '>',
    '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'W', 'X',
    'Y', 'Z', '!', '"', 'a', 'b', 'c', 'd', "e", 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '{', '|', '}', '~']

model = load_model(MODEL_PATH)
recognition_results = []

def text_recognition(processed_img):
  return