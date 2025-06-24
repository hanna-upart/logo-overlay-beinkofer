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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return JSONResponse(content={"status": "OK", "message": "Logo API läuft"})

@app.post("/add-logo")
async def add_logo(image: UploadFile = File(...)):
    logo_path = "logo.png"
    if not os.path.exists(logo_path):
        return JSONResponse(content={"error": f"Logo-Datei fehlt: {logo_path}"}, status_code=500)

    try:
        logo = Image.open(logo_path).convert("RGBA")
        original = Image.open(image.file).convert("RGBA")
    except Exception as e:
        return JSONResponse(content={"error": f"Bildfehler: {str(e)}"}, status_code=500)

    # Logo ggf. skalieren
    max_logo_width = int(original.width * 0.2)
    if logo.width > max_logo_width:
        ratio = max_logo_width / logo.width
        resized_logo = logo.resize(
            (int(logo.width * ratio), int(logo.height * ratio)), Image.ANTIALIAS
        )
    else:
        resized_logo = logo

    # Platzierung: unten rechts
    margin = 30
    position = (
        original.width - resized_logo.width - margin,
        original.height - resized_logo.height - margin
    )

    combined = original.copy()
    combined.paste(resized_logo, position, resized_logo)

    img_byte_arr = io.BytesIO()
    combined.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return StreamingResponse(img_byte_arr, media_type="image/png")
