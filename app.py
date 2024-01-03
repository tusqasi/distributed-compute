import logging
import base64
from io import BytesIO

# import requests
from fastapi import BackgroundTasks, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

STORAGE_SERVICE_URL = "http://localhost:4000/api/files/upload"

logger = logging.getLogger("uvicorn.error")
logger.info("Logger Up")
app = FastAPI(
    debug=True,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_image(content_type: str) -> bool:
    return any(content_type.find(ext) for ext in ["png", "jpeg", "jpg", "gif", "webp"])


@app.post("/scale")
async def image_scale(
    file: UploadFile, 
    scale: float,
):

    if not is_image(file.content_type):
        print("not image")
        return "notimage"

    img = Image.open(file.file)
    mem_file = BytesIO()
    resized = img.resize((int(img.width*scale), int(img.height*scale)))
    resized.save(mem_file,'png')
    mem_file.seek(0)
    return {"image": base64.b64encode(mem_file.read())}

