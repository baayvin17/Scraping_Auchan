import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.0"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.mydb

collection = database.get_collection("phones")


# Fonction d'aide 
def phone_helper(phone) -> dict:
    return {
        "id": str(phone["_id"]),
        "title": str(phone["title"]),
        "price": str(phone["price"]),
        "rating": str(phone["rating"]),
        "status": str(phone["status"]),
    }

#  Récupération de tous les téléphones dans la base de données
async def retrieve_phones():
    phones = []
    async for phone in collection.find():
        phones.append(phone_helper(phone))
    return phones


# Ajout d'un nouveau téléphone dans la base de données
async def add_phone(data: dict) -> dict:
    phone = await collection.insert_one(data)
    new_phone = await collection.find_one({"_id": phone.inserted_id})
    return phone_helper(new_phone)


# Récupération d'un téléphone avec un ID correspondant
async def retrieve_phone(id: str) -> dict:
    phone = await collection.find_one({"_id": ObjectId(id)})
    if phone:
        return phone_helper(phone)


# Mise à jour d'un téléphone avec un ID correspondant
async def update_phone(id: str, data: dict):
    #  Retourne False si une requête vide est envoyée.
    if len(data) < 1:
        return False
    phone = await collection.find_one({"_id": ObjectId(id)})
    if phone:
        updated_phone = await collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_phone:
            return True
        return False


# Suppression d'un téléphone de la base de données
async def delete_phone(id: str):
    phone = await collection.find_one({"_id": ObjectId(id)})
    if phone:
        await collection.delete_one({"_id": ObjectId(id)})
        return True
