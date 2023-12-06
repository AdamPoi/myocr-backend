from pydantic import BaseModel


class KTPImg(BaseModel):
    filename: str

class KTPData(BaseModel):
    # id:str
    # cardImageUrl:str
    cardPhotoUrl:str
    # nik:str
    # name:str
    # birthPlace:str
    # birthDate:str
    # gender:str
    # bloodType:str
    # streetAdress:str
    # rtNumber:str
    # rwNumber:str
    # # keluarahan/desa
    # village:str
    # # kecamatan
    # subDistrict:str
    # # kabupaten/kota
    # district:str
    # religion:str
    # maritalStatus:str
    # job:str
    # nationality:str
    # validUntil:str