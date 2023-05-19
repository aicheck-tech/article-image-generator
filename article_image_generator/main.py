import logging
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from article_image_generator.backend.text_processing import text_processing
from article_image_generator.settings import *


app = FastAPI()
app.mount("/assets", StaticFiles(directory="public/assets"), name="static")


class TextToPromptRequest(BaseModel):
    text_for_processing: str
    tags: list[str]


@app.get("/", response_class=FileResponse)
def main():
    return "public/index.html"


@app.post("/backend/text-to-prompts", response_class=JSONResponse)
def text_to_prompt_response(
                        text_and_tags: TextToPromptRequest
                        ) -> JSONResponse:
    text_for_processing = text_and_tags.text_for_processing
    tags = text_and_tags.tags
    prompt = text_processing().text_to_tagged_prompt(text_for_processing, tags)

    return JSONResponse(status_code=200, content={"prompt": prompt})


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.DEBUG if DEBUG else logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename="fastapi-dev.log",
        filemode="w"
    )
    uvicorn.run("main:app", port=8001, workers=1)
