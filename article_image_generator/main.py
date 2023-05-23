import logging
from pydantic import BaseModel
from typing import List, Literal, Dict, Union
from pathlib import Path
import io
import base64

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from article_image_generator.backend.pipeline import load_pipeline_from_keywords, load_pipeline_by_summarization
from article_image_generator.settings import DEBUG, IMAGE_STYLES

PATH = Path(__file__).parent/"public"

app = FastAPI()
app.mount("/assets", StaticFiles(directory=PATH/"assets"), name="static")

class TextToPromptRequest(BaseModel):
    text_for_processing: str
    image_look: Literal["realistic", "cinematic", "cartoon", "sketch"]


@app.get("/", response_class=FileResponse)
def main():
    return PATH/"index.html"


@app.post("/backend/text-to-image", response_class=JSONResponse)
def text_to_image_response(
                        text_and_look: TextToPromptRequest
                        ) -> JSONResponse:
    text_for_processing = text_and_look.text_for_processing
    image_look = text_and_look.image_look
        
    article_image_generator = load_pipeline_by_summarization()
    output: Dict[str, Union[bytes, float, str]] = article_image_generator.main(text_for_processing, IMAGE_STYLES[image_look])

    image = output["pil_image"]
    image_byte_arr = io.BytesIO()
    image.save(image_byte_arr, format='JPEG')
    image_bytes = image_byte_arr.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    return JSONResponse(status_code=200, content={
        "prompt": output["prompt"],
        # "confidence": float(output["confidence"]),
        "image_base64": image_base64
    })


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.DEBUG if DEBUG else logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename="fastapi-dev.log",
        filemode="w"
    )
    
    uvicorn.run("article_image_generator.main:app", port=8001, workers=1)
