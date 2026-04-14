from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
import os

app = FastAPI()

STORAGE_DIR = "./Data/Chunks"
os.makedirs(STORAGE_DIR, exist_ok=True)


@app.post("/store_chunk")
async def store_chunk(
        file : UploadFile, 
        filename: str = Form(...), 
        chunk_index: int = Form(...)) :
    path = os.path.join(STORAGE_DIR, f"{filename}_chunk_{chunk_index}")
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"status": "stored", "chunk": file.filename}

@app.get("/get_chunk/{filename}/{chunk_index}")
def get_chunk(filename: str, chunk_index: int) :
    path = os.path.join(STORAGE_DIR, f"{filename}_chunk_{chunk_index}")
    if not os.path.exists(path):
        return {"error": "not found"}
    with open(path, "rb") as f:
        data = f.read()
    return FileResponse(
        path, 
        media_type="application/octet-stream",
        filename=f"{filename}_chunk_{chunk_index}"
    )

@app.get("/delete_chunk/{filename}/{chunk_index}")
def delete_chunk(filename : str, chunk_index : int) :
    path = os.path.join(STORAGE_DIR, f"{filename}_chunk_{chunk_index}")
    if os.path.exists(path):
        os.remove(path)
        return {"status": "ok"}
    else :
        return {"status": "error"}


@app.get("/health")
def health():
    return {"status": "ok"}