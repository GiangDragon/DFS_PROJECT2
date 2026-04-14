import requests, os

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

from Utils.Merge import merge_chunks
from Utils.Split import split_file
from Dispenser.Dispenser import select_node
from Server.metadata import save_metadata, get_metadata, delete_metadata

app = FastAPI()

@app.post("/upload")
async def upload(file : UploadFile) :
    metadata = []
    #read file
    filename = file.filename
    with open(filename, "wb") as f:
        f.write(await file.read())
    
    #split file into chunks
    chunks = split_file(filename)
    numChunks = 0

    for chunk in chunks :
        numChunks+=1
        #select destination node and send chunk
        nodes = select_node()
        metadata.append({
            "chunk_index": numChunks,
            "nodes": nodes
        })
        data = {
            "filename": filename,
            "chunk_index": numChunks
        }
        for node in nodes :
            with open(chunk, "rb") as f:
                post_chunk = {"file": (chunk, f)}
                r = requests.post(
                    node + "/store_chunk", 
                    files=post_chunk, 
                    data=data
                )
                if r.status_code != 200:
                    print(f"FAIL upload chunk {numChunks} to {node}")
    save_metadata(filename, metadata)
    return {"status" : "uploaded"}


@app.get("/download/{filename}")
async def download(filename : str) :
    metadata = get_metadata(filename)
    output_file = "download_" + filename
    chunk_files = []
    for chunk in metadata:
        found_chunk = 0
        for node in chunk["nodes"] :
            r = requests.get(f"{node}/get_chunk/{filename}/{chunk['chunk_index']}")
            if r.status_code == 200 :
                chunk_files.append(r.content)
                found_chunk = 1
                break
        if(found_chunk == 0) :
            print(f"CANNOT FIND CHUNK : {chunk['chunk_index']}")
    merge_chunks(chunk_files, output_file)
    return FileResponse(output_file, filename=output_file)
    
@app.delete("/delete/{filename}")
async def delete(filename : str) :
    metadata = get_metadata(filename)
    for chunk in metadata:
        for node in chunk["nodes"]:
            requests.get(f"{node}/delete_chunk/{filename}/{chunk['chunk_index']}")
    delete_metadata(filename)
    return {"status": "ok"}

@app.post("/update")
async def update(file : UploadFile) :
    await delete(file.filename)
    await upload(file)
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}

