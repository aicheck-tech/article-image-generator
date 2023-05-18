import logging
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.textProcessing import text_processing

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename="fastapi-dev.log",
    filemode="w"
)

app = FastAPI()
app.mount("/assets", StaticFiles(directory="public/assets"), name="static")

text_processor = text_processing()

class TextToPromptRequest(BaseModel):
    text_for_processing: str
    tags: list


@app.get("/", response_class=FileResponse)
def main():
    return "public/index.html"

@app.get("/favicon.ico", response_class=FileResponse)
def favicon():
    return "public/favicon.ico"

@app.post("/backend/textToPrompt", response_class=JSONResponse)
def text_to_prompt_response(
    text_and_tags: TextToPromptRequest
    ) -> JSONResponse:
    text_for_processing = text_and_tags.text_for_processing
    tags = text_and_tags.tags
    prompt = text_processor.text_to_tagged_prompt(text_for_processing, tags)

    return JSONResponse(status_code=200, content={"prompt": prompt})

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        port=8001, 
        workers=1
        )
