from app.db import create_db, drop_db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import image_record, label
from decouple import config
import os


def initialize_env_vars():
    """
    Initialize environment variables
    :return:
    """
    env_variables = [
        "DATABASE_URL",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GCP_BUCKET_NAME",
    ]
    for env_var in env_variables:
        if not os.getenv(env_var):
            os.environ[env_var] = config(env_var)


initialize_env_vars()
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World from docker"}


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

app.include_router(
    label.router,
    prefix="/labels",
    tags=["labels"],
    responses={404: {"description": "Not found"}},
)
