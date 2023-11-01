from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import FileResponse
from logging.config import dictConfig
import time
import random
import subprocess
import logging


log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "foo-logger": {"handlers": ["default"], "level": "DEBUG"},
    },
}
dictConfig(log_config)

logger = logging.getLogger("foo-logger")
app = FastAPI(
    debug=True,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.debug(f"{process_time =}")
    return response


def is_image(content_type: str) -> bool:
    return content_type.find("image")
    """ return any( """
    """     [content_type.find(ext)  """
    """      for ext in ["png", "jpeg", "jpg", "gif", "webp"]] """
    """ ) """


@app.post("/scale")
async def image_scale(file: UploadFile, scale):
    if not is_image(file.content_type):
        return "notimage"
    with open(f"./scratch/{file.filename}", "wb+") as fp:
        fp.write(file.file.read())
    time.sleep(random.random() * random.randint(1, 3))
    cmd = [
        "convert",
        "./scratch/" + file.filename,
        f"-resize {scale}%",
        "./scaled/scaled_" + file.filename,
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
    time.sleep(random.random() * random.randint(1, 2))

    return FileResponse(f"./scaled/scaled_{file.filename}")
