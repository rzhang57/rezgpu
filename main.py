from fastapi import FastAPI
from pydantic import BaseModel
from services.ig_client import *

app = FastAPI()

class RepostRequest(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/repost")
async def repost(payload: RepostRequest):
    cl = get_ig_client()
    path = download_video_media(cl, payload.url)
    print("path: {path}")
    upload_video(cl, path)
    return {"status": "uploaded", "path": path}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)