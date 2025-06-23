from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image
import io

app = FastAPI()

# CORS-Freigabe für ALLE Domains (zum Testen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logo laden
logo = Image.open("Logo blau.jpg").convert("RGBA")

@app.get("/")
def root():
    return JSONResponse(content={"message": "Logo API is running"})

@app.post("/add-logo")
async def add_logo(image: UploadFile = File(...)):
    original = Image.open(image.file).convert("RGBA")
    max_logo_width = int(original.width * 0.2)
    if logo.width > max_logo_width:
        ratio = max_logo_width / logo.width
        resized_logo = logo.resize((int(logo.width * ratio), int(logo.height * ratio)), Image.ANTIALIAS)
    else:
        resized_logo = logo
    margin = 30
    position = (
        original.width - resized_logo.width - margin,
        original.height - resized_logo.height - margin
    )
    combined = original.copy()
    combined.paste(resized_logo, position, resized_logo)

    img_byte_arr = io.BytesIO()
    combined.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return StreamingResponse(img_byte_arr, media_type="image/png")
