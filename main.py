from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import router as api_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fe-the-best-employees.vercel.app"],  # Izinkan domain frontend Anda
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode
    allow_headers=["*"],  # Izinkan semua header
)

app.include_router(api_router, prefix="/api/v1")
