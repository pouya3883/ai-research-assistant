from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.documents import router as documents_router

app = FastAPI()

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(documents_router)


@app.get("/")
def root():
    return {"message": "AI Research Assistant API"}
