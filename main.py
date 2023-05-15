import sys

import uvicorn

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/assets", StaticFiles(directory="public/assets"), name="static")

@app.get("/", response_class=FileResponse)
def main():
    return "public/index.html"

def shutdown_handler(sig, frame):
    print("Shutting down server...")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ('dev', '--dev', '-d'):
        print("dev")
        import signal
        signal.signal(signal.SIGINT, shutdown_handler)
        uvicorn.run("main:app", port=8001, reload=True, workers=1)
    else:
        uvicorn.run("main:app", port=8001, workers=1)