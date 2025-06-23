from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image
import io
import os

app = FastAPI()

# CORS für Browser-Uploads
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für Tests erlaubt alles
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logo prüfen und laden
logo_path = "logo.png"
if not os.path.exists(logo_path):
    raise RuntimeError(f"Logo-Datei fehlt: {logo_path}")

logo = Image.open(logo_path).convert("RGBA")

# Test-Route für "läuft"-Check
@app.get("/")
def root():
    return JSONResponse(content={"status": "OK", "message": "Logo API läuft"})

# Hauptfunktion zum Logo-Einfügen
@app.post("/add-logo")
async def add_logo(image: UploadFile = File(...)):
    original = Image.open(image.file).convert("RGBA")
    
    # Logo ggf. skalieren
    max_logo_width = int(original.width * 0.2)
    if logo.width > max_logo_width:
        ratio = max_logo_width / logo.width
        resized_logo = logo.resize(
            (int(logo.width * ratio), int(logo.height * ratio)), Image.ANTIALIAS
        )
    else:
        resized_logo = logo

    # Platzi
