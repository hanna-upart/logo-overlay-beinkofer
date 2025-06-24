from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os

# Starte FastAPI und aktiviere CORS für alle Domains (du kannst das später einschränken)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaube alle Ursprünge (z. B. dein GPT)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lade das Logo (muss im Projektordner liegen, z. B. "logo.png")
logo_path = "logo.png"
if not os.path.exists(logo_path):
    raise RuntimeError(f"Logo-Datei nicht gefunden: {logo_path}")

logo = Image.open(logo_path).convert("RGBA")

# API-Endpunkt: Bild hochladen, Logo einfügen, Bild zurückgeben
@app.post("/add-logo")
async def add_logo(image: UploadFile = File(...)):
    original = Image.open(image.file).convert("RGBA")

    # Logo ggf. skalieren (max 20% der Originalbildbreite)
    max_logo_width = int(original.width * 0.2)
    if logo.width > max_logo_width:
        ratio = max_logo_width / logo.width
        resized_logo = logo.resize(
            (int(logo.width * ratio), int(logo.height * ratio)),
            resample=Image.LANCZOS
        )
    else:
        resized_logo = logo

    # Position des Logos (rechts unten mit etwas Abstand)
    margin = 30
    position = (
        original.width - resized_logo.width - margin,
        original.height - resized_logo.height - margin
    )

    # Kombiniere Originalbild + Logo
    combined = original.copy()
    combined.paste(resized_logo, position, resized_logo)

    # Bild als PNG streamen
    img_byte_arr = io.BytesIO()
    combined.save(img_byte_arr, format='PNG')
  
