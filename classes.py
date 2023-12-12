from pydantic import BaseModel


class KTPImg(BaseModel):
    filename: str

class KTPData(BaseModel):
    # id:str
    # cardImageUrl:str
    # cardPhoto:bytes or null
    nik:str or null
    name:str or null
    birthPlace:str or null
    birthDate:str or null
    gender:str or null
    bloodType:str or null
    streetAddress:str or null
    rtNumber:str or null
    rwNumber:str or null
    # # kelurahan/desa
    village:str or null
    # # kecamatan
    subDistrict:str or null
    # # kabupaten/kota
    district:str or null
    religion:str or null
    maritalStatus:str or null
    job:str or null
    nationality:str or null
    validUntil:str or null