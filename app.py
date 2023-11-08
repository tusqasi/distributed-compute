import base64
import logging
import os
import subprocess
import uuid

import requests
from fastapi import BackgroundTasks, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

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
    file: UploadFile, scale: int, user_id: str, background_tasks: BackgroundTasks
):
    filename = file.filename.replace(" ", "_")

    # I am testing this setup, i am uploading a single file multiple times which is not expected
    # having randomess in the filename will alleviate conflicts
    random_id = uuid.uuid4()
    if not is_image(file.content_type):
        print("not image")
        return "notimage"

    original_file = file.file.read()

    with open(f"./scratch/{random_id}{filename}", "xb") as fp:
        fp.write(original_file)

    cmd = f"convert ./scratch/{random_id}{filename} -resize {scale}% ./scaled/{random_id}{filename}"

    subprocess.run(cmd, shell=True)

    def send_images_to_storage():
        logger.info("Sending image to Storage service")
        try:
            ## CUrl is just *chefs-kiss*
            res = subprocess.run(
                f"curl -q -X POST \
                    -F 'file=@./scratch/{random_id}{filename}' \
                    'http://127.0.0.1:4000/api/files/upload?scale={scale}&user_id={user_id}' ",
                shell=True,
                check=True,
                capture_output=True,
            )
            logger.info("Sent image to Storage service: %s ", res.stdout.decode())
        except requests.exceptions.ConnectionError:
            logger.error(
                "Can not connect to File Storage Service. Is the service running?"
            )
        finally:
            logger.info("Removing temp files")
            os.remove(f"./scratch/{random_id}{filename}")
            os.remove(f"./scaled/{random_id}{filename}")

    with open(f"./scaled/{random_id}{filename}", "rb") as fp:
        background_tasks.add_task(
            send_images_to_storage,
        )
        return {
            "image": base64.b64encode(fp.read()),
            "type": file.content_type,
        }
