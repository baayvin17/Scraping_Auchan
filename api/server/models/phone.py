from typing import Optional
from pydantic import BaseModel, Field


class PhoneModel(BaseModel):
    titre: str = Field(...)
    prix: str = Field(...)
    status: str = Field(...)
    rating: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "titre": "test_titre",
                "prix": "test_prix",
                "status": "test_status",
                "rating": 4.5,
            }
        }


class UpdatePhoneModel(BaseModel):
    titre: str = Field(...)
    prix: str = Field(...)
    status: float = Field(...)
    rating: Optional[float] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "titre": "update_test_titre",
                "prix": "update_test_prix",
                "status": "update_test_status",
                "rating": 4.5,
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
