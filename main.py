from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root() :
    return "Hello World"

@app.get("/test")
def test() :
    return "Hello this is test"

