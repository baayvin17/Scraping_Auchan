from ast import List
from fastapi import FastAPI, HTTPException, Body, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, Field, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from enum import Enum

app = FastAPI()

# Configuration de la connexion à MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["phones"]  # Modifier le nom de la collection

# Configuration de Jinja2 pour les templates HTML
templates = Jinja2Templates(directory="templates")


class PhoneModel(BaseModel):
    title: str
    price: float
    rating: Optional[float]  


class UpdatePhoneModel(BaseModel):
    title: Optional[str]
    price: Optional[float]
    rating: Optional[float]  


class PhoneCollection(BaseModel):
    phones: List[PhoneModel]


@app.post("/phones/", response_description="Ajouter un nouveau téléphone Auchan", response_model=PhoneModel)
async def create_phone(phone: PhoneModel = Body(...)):
    result = await collection.insert_one(phone.dict())
    return PhoneModel(**phone.dict(), id=str(result.inserted_id))


@app.get("/phones/", response_description="Lister tous les téléphones Auchan", response_model=PhoneCollection)
async def list_phones():
    phones = await collection.find().to_list(length=1000)
    return PhoneCollection(phones=[PhoneModel(**phone, id=str(phone["_id"])) for phone in phones])


@app.get("/phones/{id}", response_description="Obtenir un seul téléphone Auchan", response_model=PhoneModel)
async def show_phone(id: str):
    phone = await collection.find_one({"_id": ObjectId(id)})
    if phone:
        return PhoneModel(**phone, id=str(phone["_id"]))
    raise HTTPException(status_code=404, detail=f"Téléphone {id} non trouvé")


@app.put("/phones/{id}", response_description="Mettre à jour un téléphone Auchan", response_model=PhoneModel)
async def update_phone(id: str, phone: UpdatePhoneModel = Body(...)):
    update_dict = {k: v for k, v in phone.dict().items() if v is not None}
    if update_dict:
        updated_phone = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_dict},
            return_document=True,
        )
        if updated_phone:
            return PhoneModel(**updated_phone, id=str(updated_phone["_id"]))
        raise HTTPException(status_code=404, detail=f"Téléphone {id} non trouvé")
    existing_phone = await collection.find_one({"_id": ObjectId(id)})
    if existing_phone:
        return PhoneModel(**existing_phone, id=str(existing_phone["_id"]))
    raise HTTPException(status_code=404, detail=f"Téléphone {id} non trouvé")


@app.delete("/phones/{id}", response_description="Supprimer un téléphone Auchan", status_code=204)
async def delete_phone(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Téléphone {id} non trouvé")
