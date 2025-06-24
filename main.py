from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os

# 🟦 Starte FastAPI-App & aktiviere CORS für alle Domains
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Oder schränke das auf deine Domain ein
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📂 Lade Logo
logo_path = "logo.png"
if not os.path.exists(logo_path):
    raise RuntimeError(f"Logo-Datei nicht gefunden: {logo_path}")

logo = Image.open(logo_path).convert("RGBA")

# 🎯 POST-Route zum Hochladen & Vera
