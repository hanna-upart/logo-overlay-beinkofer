from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import os

app = FastAPI()

# CORS aktivieren für alle Domains (optional, aber nützlich für GPT-Verbindung)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logo laden
LOGO_PATH = "logo.png"
if not os.path.exists(LOGO_PATH):
    raise RuntimeError(f"Logo-Datei nicht gefunden: {LOGO_PATH}")

logo = Image.open(LOGO_PATH).convert("RGBA")

@app.post("/add-logo")
async def add_logo(image: UploadFile = File(...)):
    # Bild laden
    original = Image.open(image.file).convert("RGBA")

    # Logo verkleinern auf max 20 % der Breite
    max_logo_width = int(original.width * 0.2)
    ratio = max_logo_width / logo.width
    new_logo = logo.resize(
        (int(logo.width * ratio), int(logo.height * ratio)),
        resample=Image.LANCZOS
    )

    # Position unten rechts mit Abstand
    margin = 30
    position = (
        original.width - new_logo.width - margin,
        original.height - new_logo.height - margin
    )

    # Logo einfügen
    result = original.copy()
    result.paste(new_logo, position, new_logo)

    # Bild als PNG zurückgeben
    img_bytes = io.BytesIO()
    result.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/png")
