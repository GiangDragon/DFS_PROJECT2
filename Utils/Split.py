import os
CHUNK_SIZE = 1024*1024

def split_file(file_path) :
    chunks = []
    index = 0

    with open(file_path, "rb") as f:
        while True :
            data = f.read(CHUNK_SIZE)
            if not data :
                break
            chunk_name = f"{file_path}_chunk_{index}"
            with open(chunk_name, "wb") as c:
                c.write(data)
            chunks.append(chunk_name)
            index += 1
    return chunks
