from fastapi import FastAPI

from .db import models
from .db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, auth, passport, qt_token, available_doc, driver_license, health_insurance, insurance_number

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(passport.router)
app.include_router(qt_token.router)
app.include_router(available_doc.router)
app.include_router(driver_license.router)
app.include_router(health_insurance.router)
app.include_router(insurance_number.router)


@app.get("/")
def read_root():
    return {"State": "Working"}
