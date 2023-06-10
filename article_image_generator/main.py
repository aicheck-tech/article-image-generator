import logging
from pydantic import BaseModel
from typing import Literal, Dict, Union
from pathlib import Path
import io
import base64

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from article_image_generator.backend.pipeline import load_pipeline_from_keywords, load_pipeline_by_summarization
from article_image_generator.settings import \
    DEBUG, IMAGE_STYLES, FASTAPI_HOST, FASTAPI_PORT, FASTAPI_WORKERS, MAX_STEPS, MIN_STEPS, MAX_SAMPLES, MIN_SAMPLES

PATH = Path(__file__).parent/"public"

app = FastAPI()
app.mount("/assets", StaticFiles(directory=PATH/"assets"), name="static")

aig_keywords = load_pipeline_from_keywords()
aig_summarization = load_pipeline_by_summarization()


class TextToPromptRequest(BaseModel):
    text_for_processing: str
    image_look: Literal["realistic", "cinematic", "cartoon", "sketch"]
    steps: int = 30
    samples: int = 1


@app.get("/", response_class=FileResponse)
def main():
    return PATH/"index.html"


@app.get("/contact", response_class=FileResponse)
def contact_page():
    return PATH/"pages"/"contact.html"


def text_to_image(main_function, text_and_look: TextToPromptRequest) -> JSONResponse:
    text_for_processing = text_and_look.text_for_processing[:2000]  # Limit text to 2000 characters
    image_look = text_and_look.image_look
    steps = max(min(text_and_look.steps, MAX_STEPS), MIN_STEPS)  # Limit steps between 20 and 90
    samples = max(min(text_and_look.samples, MAX_SAMPLES), MIN_SAMPLES)  # Limit samples between 1 and 4
    output: Dict[str, Union[bytes, float, str]] = main_function(
        text_for_processing,
        IMAGE_STYLES[image_look],
        steps=steps,
        samples=samples
        )
    images = output.get("pil_images", None)
    if images is None:
        return JSONResponse(status_code=451, content={
            "error": output["error"]
        })
    images_base64 = []
    for image in images:
        image_byte_arr = io.BytesIO()
        image.save(image_byte_arr, format='JPEG')
        image_bytes = image_byte_arr.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        images_base64.append(image_base64)
        logging.info(f"Image base64: {image_base64[:50]}...")
    return JSONResponse(status_code=200, content={
        "prompt": output["prompt"],
        "images_base64": images_base64
    })


@app.post("/backend/text-to-image/summarization", response_class=JSONResponse)
def text_to_image_response_summarization(text_and_look: TextToPromptRequest) -> JSONResponse:
    return text_to_image(aig_summarization.main, text_and_look)


@app.post("/backend/text-to-image/keywords", response_class=JSONResponse)
def text_to_image_response_keywords(text_and_look: TextToPromptRequest) -> JSONResponse:
    return text_to_image(aig_keywords.main, text_and_look)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.DEBUG if DEBUG else logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename="fastapi-dev.log",
        filemode="w"
    )

    uvicorn.run("article_image_generator.main:app", host=FASTAPI_HOST, port=FASTAPI_PORT, workers=FASTAPI_WORKERS)
