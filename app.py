from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import time
import random
import subprocess
import base64

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

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
async def image_scale(file: UploadFile):
    scale = 30
    filename = file.filename.replace(" ", "_")

    print(f"{file.content_type=}")
    print(f"{filename=}")

    if not is_image(file.content_type):
        print("not image")
        return "notimage"

    with open(f"./scratch/{filename}", "wb+") as fp:
        fp.write(file.file.read())

    """ time.sleep(random.random() * random.randint(1, 3)) """
    cmd = [
        "convert",
        "./scratch/" + filename,
        f"-resize {scale}%",
        "./scaled/scaled_" + filename,
    ]
    _p: str = (
        subprocess.Popen(
            " ".join(cmd),
            stdout=subprocess.PIPE,
            shell=True,
        )
        .communicate()[0]
        .decode()
    )
    """ time.sleep(random.random() * random.randint(1, 2)) """

    with open(f"./scaled/scaled_{filename}", "rb") as fp:
        return {
            "image": base64.b64encode(fp.read()),
            "type": file.content_type,
        }

    """ return FileResponse(f"./scaled/scaled_{filename}") """
