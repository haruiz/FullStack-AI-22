from app.db import create_db, drop_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import image_record

app = FastAPI()

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.on_event("shutdown")
def shutdown_event():
    """
    Drop the database
    :return:
    """
    drop_db()


@app.on_event("startup")
def startup_event():
    """
    Create the database
    :return:
    """
    create_db()


app.include_router(
    image_record.router,
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)


@app.get("/")
def home():
    return {"message": "Hello World from docker"}
