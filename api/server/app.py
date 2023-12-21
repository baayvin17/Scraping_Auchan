from fastapi import FastAPI

from server.routes.phone import router as PhoneRouter  

app = FastAPI()

app.include_router(PhoneRouter, tags=["Phone"], prefix="/phones")  

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this app!"}
