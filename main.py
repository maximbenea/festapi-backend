import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64, re, os
import logging
from gemini_api import gemini_request

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)


class Image(BaseModel):
    image_base64: str

class Message(BaseModel):
    message: str

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print("Incoming request:", request.method, request.url, flush=True)
    response = await call_next(request)
    return response

latest_message = ""

@app.post("/upload-frame")
async def upload_image(image: Image):

    file_path = "image.jpg"
    if not os.path.isfile(file_path):
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image.image_base64[23:]))

    print(gemini_request())
    gemini_response = gemini_request()

    global latest_message
    latest_message = gemini_response

    os.remove(file_path)

    return {"image_base64": image.image_base64}

@app.get("/chat-messages", response_model=Message)
async def get_output():
    return Message(message=latest_message)
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)