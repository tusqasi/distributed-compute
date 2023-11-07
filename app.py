from fastapi import FastAPI, UploadFile, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests
import time
import random
import subprocess
import base64
import uuid
import logging


STORAGE_SERVICE_URL = "http://localhost:4000/api/files/upload",

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
    return any(
        [content_type.find(ext) for ext in ["png", "jpeg", "jpg", "gif", "webp"]]
    )


@app.post("/scale")
async def image_scale(file: UploadFile, scale: int, background_tasks: BackgroundTasks):
    filename = file.filename.replace(" ", "_")

    if not is_image(file.content_type):
        print("not image")
        return "notimage"
    original_file = file.file.read()
    with open(f"./scratch/{filename}", "wb+") as fp:
        fp.write(original_file)

    time.sleep(random.random() * random.randint(1, 3))
    cmd = [
        "convert",
        "./scratch/" + filename,
        f"-resize {scale}%",
        "./scaled/scaled_" + filename,
    ]

    cmd = f"convert ./scratch/{filename} -resize {scale}% ./scaled/scaled_{filename}"

    subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        shell=True,
    )
    time.sleep(random.random() * random.randint(1, 2))

    def send_images_to_storage():
        logger.info("Sending image to Storage service")
        requests.post(
            STORAGE_SERVICE_URL,
            json={
                "scale": scale,
                "file": base64.b64encode(original_file).decode(),
                "user_id": "502b2c72-fd13-4c1d-a9e1-f0e82c8b7459",
                "filename": filename,
            },
        )
        logger.info("Sent image to Storage service")

    with open(f"./scaled/scaled_{filename}", "rb") as fp:
        background_tasks.add_task(
            send_images_to_storage,
        )
        return {
            "image": base64.b64encode(fp.read()),
            "type": file.content_type,
        }

