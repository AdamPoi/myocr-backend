from pydantic import BaseModel

class KTPData(BaseModel):
    # id:str
    ktp_img: str
    face_img:str
    nik:str
    name:str
    birthPlace:str
    birthDate:str
    gender:str
    bloodType:str
    streetAddress:str
    rtNumber:str
    rwNumber:str
    # # kelurahan/desa
    village:str
    # # kecamatan
    subDistrict:str
    # # kabupaten/kota
    district:str
    religion:str
    maritalStatus:str
    job:str
    nationality:str
    validUntil:str