from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_phone,
    delete_phone,
    retrieve_phone,
    retrieve_phones,
    update_phone,
)
from server.models.phone import (
    ErrorResponseModel,
    ResponseModel,
    PhoneModel,
    UpdatePhoneModel,
)

router = APIRouter()

# Ajout d'un téléphone dans la base de données
@router.post("/", response_description="Phone data added into the database")
async def add_phone_data(phone: PhoneModel = Body(...)):
    phone = jsonable_encoder(phone)
    new_phone = await add_phone(phone)
    return ResponseModel(new_phone, "Phone added successfully.")

# Récupération de tous les téléphones depuis la base de données
@router.get("/", response_description="Phones retrieved")
async def get_phones_data():
    phones = await retrieve_phones()
    if phones:
        return ResponseModel(phones, "Phones data retrieved successfully")
    return ResponseModel(phones, "Empty list returned")

# Récupération des données d'un téléphone spécifique
@router.get("/{id}", response_description="Phone data retrieved")
async def get_phone_data(id):
    phone = await retrieve_phone(id)
    if phone:
        return ResponseModel(phone, "Phone data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Phone doesn't exist.")

# Mise à jour des données d'un téléphone spécifique
@router.put("/{id}")
async def update_phone_data(id: str, req: UpdatePhoneModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_phone = await update_phone(id, req)
    if updated_phone:
        return ResponseModel(
            "Phone with ID: {} updated successfully".format(id),
            "Phone data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the phone data.",
    )

# Suppression des données d'un téléphone spécifique
@router.delete("/{id}", response_description="Phone data deleted from the database")
async def delete_phone_data(id: str):
    deleted_phone = await delete_phone(id)
    if deleted_phone:
        return ResponseModel(
            "Phone with ID: {} removed".format(id), "Phone deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Phone with id {0} doesn't exist".format(id)
    )
    